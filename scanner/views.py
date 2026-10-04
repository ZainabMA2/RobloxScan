from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView,DeleteView,UpdateView,DetailView, TemplateView
from django.urls import reverse_lazy
from .models import RobloxProject, codeScan, securityIssue
from .engine.scanner import scan_code
from django.contrib.auth.mixins import LoginRequiredMixin
from .engine.ai_engine import explain_issues

##
class RobloxProjectListView(LoginRequiredMixin,ListView):
    model= RobloxProject
    context_object_name='projects'
    template_name='scanner/project_list.html'
    def get_queryset(self):
        return RobloxProject.objects.filter(owner=self.request.user)

class RobloxProjectDetailView(LoginRequiredMixin,DetailView):
    model =RobloxProject
    context_object_name='project'
    template_name= 'scanner/project_detail.html'
    def get_queryset(self):
        return RobloxProject.objects.filter(owner=self.request.user)

class RobloxProjectDeleteView(LoginRequiredMixin,DeleteView):
    model =RobloxProject
    template_name= 'scanner/project_delete.html'
    success_url=reverse_lazy("scanner:project_list")
    def get_queryset(self):
        return RobloxProject.objects.filter(owner=self.request.user)

class RobloxProjectCreateView(LoginRequiredMixin,CreateView):
    model= RobloxProject
    fields= ['name', 'description']
    template_name='scanner/project_create.html'
    success_url= reverse_lazy('scanner:project_list')
    def form_valid(self, form): #يشغلها لمن الفورم يكون صح
        form.instance.owner =self.request.user #اللي يستخدم الفورم الحين
        return super().form_valid(form)

class RobloxProjectUpdateView(LoginRequiredMixin,UpdateView):
    model= RobloxProject
    fields= ['name', 'description']
    template_name='scanner/project_update.html'
    success_url= reverse_lazy('scanner:project_list')
    def get_queryset(self):
        return RobloxProject.objects.filter(owner=self.request.user)

####
class CodeScanCreateView(LoginRequiredMixin,CreateView):
    model= codeScan
    fields=['code']
    template_name='scanner/scan_create.html'

    def form_valid(self, form): 
        project = get_object_or_404(
            RobloxProject,
            pk=self.kwargs["pk"],
            owner =self.request.user 
        )

        form.instance.project =project
        response = super().form_valid(form)

        code = self.object.code
        issues,score =scan_code(code)
        for issue in issues:
            securityIssue.objects.create(
                scan =self.object,
                ruleID = issue["ruleID"],
                title = issue["title"],
                category = issue["category"],
                severity = issue["severity"],
                line_number = issue["line_number"],
                message = issue["message"]
            )
        self.object.score =score
        self.object.save()
        return response


    def get_success_url(self): 
        return reverse_lazy(
            'scanner:scan_result',
            kwargs={'pk':self.object.pk}
        )

class CodeScanDetailView(LoginRequiredMixin, DetailView):
    model = codeScan
    context_object_name = "scan"
    template_name = "scanner/scan_result.html"

    def get_queryset(self):
        return codeScan.objects.filter(
            project__owner=self.request.user
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        issues = self.object.issues.all()

        issues_data = []

        for issue in issues:
            issues_data.append({
                "ruleID": issue.ruleID,
                "title": issue.title,
                "category": issue.category,
                "severity": issue.severity,
                "line_number": issue.line_number,
                "message": issue.message,
            })
        ai_results = explain_issues(
            self.object.code,
            issues_data
            )
       

        context = self.get_context_data(
            object=self.object
        )
        context["ai_results"] = ai_results

        

        return self.render_to_response(context)
##
class DashboardView(LoginRequiredMixin,TemplateView):
    template_name ="scanner/dashboard.html"

    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)

        context ["projects"] =RobloxProject.objects.filter(owner=self.request.user)
        context["scans"] =codeScan.objects.filter(project__owner=self.request.user)

        return context



 