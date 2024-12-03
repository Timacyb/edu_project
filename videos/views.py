from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.utils import timezone

from .models import Category, Quiz, Videos, Yangi, Instrument, Termin
from django.views.generic import ListView, TemplateView, DetailView
from .forms import ContactForm


# Create your views here.


def videos_list(request):
    videos_list = Videos.objects.filter(status=Videos.Status.Published)
    context = {
        "videos_list": videos_list
    }

    return render(request, "videos/videos_list.html", context)


def homePageView(request):
    categories = Category.objects.all()
    videos_list = Videos.objects.filter(status=Videos.Status.Published).order_by('-publish_time')[:5]
    context = {
        'videos_list': videos_list,
        'categories': categories,
    }

    return render(request, 'videos/home.html', context)


class ContactPageView(TemplateView):
    template_name = 'videos/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            "form": form
        }
        return render(request, 'videos/contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse(
                "{% url 'home_page' %}")
        context = {
            "form": form
        }
        return render(request, 'videos/contact.html', context)


class BlogPageView(TemplateView):
    template_name = 'videos/blog.html'


class AboutPageView(TemplateView):
    template_name = 'videos/about.html'


#
# class CyberCriminalisticView(ListView):
#     model = Videos
#     template_name = 'videos/cyber_criminalistic.html'
#     context_object_name = 'cybercriminalistic'
#
#     def get_queryset(self):
#         videos = Videos.objects.filter(status=Videos.Status.Published, category__name='CyberCriminalistic')
#         # news = self.model.published.all().filter(category__name='KiberSport')
#         return videos
#
#
# class NetworkSecurityView(ListView):
#     model = Videos
#     template_name = 'videos/network_security.html'
#     context_object_name = 'networksecurity'
#
#     def get_queryset(self):
#         videos = Videos.objects.filter(status=Videos.Status.Published, category__name='NetworkSecurity')
#         # news = self.model.published.all().filter(category__name='KiberSport')
#         return videos
#
#
# class OperationSystemSecurityView(ListView):
#     model = Videos
#     template_name = 'videos/operation_system_security.html'
#     context_object_name = 'operationsystemsecurity'
#
#     def get_queryset(self):
#         videos = Videos.objects.filter(status=Videos.Status.Published, category__name='OperationSystemSecurity')
#         # news = self.model.published.all().filter(category__name='KiberSport')
#         return videos


# class PentestingView(ListView):
#     model = Videos
#     template_name = 'videos/pentesting.html'
#     context_object_name = 'pentesting'
#
#     def get_queryset(self):
#         videos = Videos.objects.filter(status=Videos.Status.Published, category__name='Pentesting')
#         # news = self.model.published.all().filter(category__name='KiberSport')
#         return videos

#
# @login_required
# @user_passes_test(lambda u: u.is_active)
# def pentesting_view(request):
#     users = User.objects.filter(is_active=True)
#     context = {
#         'users': users
#     }
#     return render(request, 'videos/pentesting.html', context)
#
#
# # @login_required
# # @user_passes_test(lambda u: u.is_active)
# # def network_view(request):
# #     users = User.objects.filter(is_active=True)
# #     context = {
# #         'users': users
# #     }
# #     return render(request, 'videos/network_security.html', context)
#
#
# @login_required
# @user_passes_test(lambda u: u.is_active)
# def operation_view(request):
#     users = User.objects.filter(is_active=True)
#     context = {
#         'users': users
#     }
#     return render(request, 'videos/operation_system_security.html', context)
#
#
# @login_required
# @user_passes_test(lambda u: u.is_active)
# def criminal_view(request):
#     users = User.objects.filter(is_active=True)
#     context = {
#         'users': users
#     }
#     return render(request, 'videos/cyber_criminalistic.html', context)


# class BaseSubadminView(LoginRequiredMixin, UserPassesTestMixin, ListView):
#     """
#     Базовый класс, который проверяет, что пользователь аутентифицирован, активен,
#     и является членом группы "Subadmin".
#     """
#
#     def test_func(self):
#         user = self.request.user
#         return user.is_active
#
#     # Дополнительные методы, если нужно, можно также разместить в этом базовом классе
class BaseSubadminView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Базовый класс, который проверяет, что пользователь аутентифицирован, активен,
    и является членом группы "Subadmin".
    """

    login_url = reverse_lazy('login_page')  # Задаем URL для перенаправления

    def test_func(self):
        user = self.request.user
        return user.is_active

    def handle_no_permission(self):
        if not self.request.user.is_active:
            return redirect(self.login_url)  # Перенаправление неактивного пользователя на login_page
        return super().handle_no_permission()


class NetworkSecurityView(BaseSubadminView):
    model = Videos
    template_name = 'videos/network_security.html'
    context_object_name = 'networksecurity'

    def get_queryset(self):
        return Videos.objects.filter(
            status=Videos.Status.Published,
            category__name='NetworkSecurity'
        )


class PentestingView(BaseSubadminView):
    model = Videos
    template_name = 'videos/pentesting.html'
    context_object_name = 'pentesting'

    def get_queryset(self):
        return Videos.objects.filter(
            status=Videos.Status.Published,
            category__name='Pentesting'
        )


class OperationSystemSecurityView(BaseSubadminView):
    model = Videos
    template_name = 'videos/operation_system_security.html'
    context_object_name = 'operationsystemsecurity'

    def get_queryset(self):
        return Videos.objects.filter(
            status=Videos.Status.Published,
            category__name='OperationSystem'
        )


class CyberCriminalisticView(BaseSubadminView):
    model = Videos
    template_name = 'videos/cyber_criminalistic.html'
    context_object_name = 'cybercriminalistic'

    def get_queryset(self):
        return Videos.objects.filter(
            status=Videos.Status.Published,
            category__name='CyberCriminal'
        )


# def videos_detail(request, id):
#     videos = get_object_or_404(Videos, id=id, status=Videos.Status.Published)
#
#     context = {
#         "videos": videos
#     }
#     return render(request, "videos/videos_detail.html", context)

# class VideoDetailView(BaseSubadminView, DetailView):
#     model = Videos
#     template_name = 'videos/videos_detail.html'
#     context_object_name = 'videos'
#
#     def get_queryset(self):
#         return Videos.objects.filter(
#             status=Videos.Status.Published,
#             category__name='CyberCriminal'
#         )

def videos_detail(request, id):
    # Проверяем, что пользователь аутентифицирован и активен
    if not request.user.is_authenticated:
        return redirect('login_page')  # Перенаправление на страницу входа, если пользователь не авторизован

    if not request.user.is_active:
        return HttpResponseForbidden("Ваш аккаунт неактивен. Пожалуйста, свяжитесь с администратором.")

    # Получаем видео только если оно опубликовано
    videos = get_object_or_404(Videos, id=id, status=Videos.Status.Published)

    context = {
        "videos": videos
    }
    return render(request, "videos/videos_detail.html", context)


class QuizListView(View):
    def get(self, request):
        quizzes = Quiz.objects.all()
        return render(request, 'videos/quiz_list.html', {'quizzes': quizzes})


class QuizView(View):
    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = quiz.questions.all()
        request.session['start_time'] = timezone.now().timestamp()
        return render(request, 'videos/quiz.html',
                      {'quiz': quiz, 'questions': questions, 'time_limit': 60})  # Укажите лимит времени в секундах

    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = quiz.questions.all()
        score = 0
        total_questions = questions.count()

        start_time = request.session.get('start_time')
        elapsed_time = timezone.now().timestamp() - start_time
        time_limit = 60  # Ограничение времени в секундах

        # Сообщение о статусе завершения теста
        if elapsed_time > time_limit:
            result_message = "Vaqt tugadi."
        else:
            result_message = "Test yakunlandi."

        # Подсчет правильных ответов
        for question in questions:
            selected_answer = request.POST.get(f"question_{question.id}")
            if selected_answer and int(selected_answer) == question.correct_answer:
                score += 1

        # Рассчет оценки в процентах
        grade = round((score / total_questions) * 100)

        return render(request, 'videos/result.html', {
            'score': score,
            'total': total_questions,
            'grade': grade,
            'message': result_message
        })


class CoursesView(TemplateView):
    template_name = 'videos/courses.html'


def yangi_list(request):
    yangi_list = Yangi.objects.filter(status=Yangi.Status.Published)
    context = {
        "yangi_list": yangi_list
    }

    return render(request, "videos/blog.html", context)


class InstrumentView(ListView):
    model = Instrument
    template_name = 'videos/instruments.html'


class TerminView(ListView):
    model = Termin
    template_name = 'videos/termins.html'


# class InstrumentView(ListView):
#     model = Instrument
#     template_name = 'videos/instruments.html'


def instrument_list(request):
    instrument_list = Instrument.objects.all()
    context = {
        "instrument_list": instrument_list
    }

    return render(request, "videos/instruments.html", context)


from django.shortcuts import render


def page_not_found(request, exception):
    return render(request, 'videos/404.html', status=404)
