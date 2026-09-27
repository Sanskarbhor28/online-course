from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Course, Lesson, Question, Choice, Submission


def popular_course_list(request):
    """View to list all available courses."""
    courses = Course.objects.all()
    context = {'course_list': courses}
    return render(request, 'onlinecourseapp/course_details_bootstrap.html', context)


def course_details(request, course_id):
    """View to display details of a specific course and its lessons."""
    course = get_object_or_404(Course, pk=course_id)
    context = {'course': course}
    return render(request, 'onlinecourseapp/course_details_bootstrap.html', context)


def exam(request, course_id):
    """View to display the exam page with questions and choices for a course."""
    course = get_object_or_404(Course, pk=course_id)
    lessons = course.lessons.all()
    
    # Collect all questions belonging to lessons in this course
    questions = Question.objects.filter(lesson__course=course)
    
    context = {
        'course': course,
        'lessons': lessons,
        'questions': questions,
    }
    return render(request, 'onlinecourseapp/exam.html', context)


def submit(request, course_id):
    """View to process submitted answers, calculate score, create Submission, and redirect to results."""
    course = get_object_or_404(Course, pk=course_id)
    
    if request.method == 'POST':
        selected_choice_ids = []
        
        # Extract selected choices from POST data
        # Form inputs can be named 'choice_<question_id>' or 'choice'
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                selected_choice_ids.append(int(value))
            elif key == 'choice':
                if isinstance(value, list):
                    selected_choice_ids.extend([int(v) for v in value])
                else:
                    selected_choice_ids.append(int(value))
                    
        # Get all selected choice objects
        selected_choices = Choice.objects.filter(id__in=selected_choice_ids)
        
        # Calculate total score
        questions = Question.objects.filter(lesson__course=course)
        score = 0.0
        total = 0.0
        
        for question in questions:
            total += float(question.grade)
            # Find selected choice IDs for this specific question
            q_selected_ids = [c.id for c in selected_choices if c.question_id == question.id]
            if question.is_get_score(q_selected_ids):
                score += float(question.grade)
                
        # Create Submission record
        user = request.user if request.user.is_authenticated else None
        submission = Submission.objects.create(
            user=user,
            course=course,
            score=score,
            total=total
        )
        submission.choices.set(selected_choices)
        submission.save()
        
        return redirect('onlinecourseapp:show_exam_result', submission_id=submission.id)
        
    return redirect('onlinecourseapp:exam', course_id=course.id)


def show_exam_result(request, submission_id):
    """View to display exam results, final score, detailed answer evaluation, and congratulations message."""
    submission = get_object_or_404(Submission, pk=submission_id)
    course = submission.course
    
    selected_choice_ids = set(submission.choices.values_list('id', flat=True))
    questions = Question.objects.filter(lesson__course=course).prefetch_related('choices')
    
    exam_results = []
    for question in questions:
        q_selected_ids = [c.id for c in submission.choices.all() if c.question_id == question.id]
        is_correct = question.is_get_score(q_selected_ids)
        
        choice_details = []
        for choice in question.choices.all():
            choice_details.append({
                'text': choice.choice_text,
                'is_correct': choice.is_correct,
                'is_selected': choice.id in selected_choice_ids
            })
            
        exam_results.append({
            'question': question.question_text,
            'grade': question.grade,
            'is_correct': is_correct,
            'choices': choice_details,
        })
        
    percentage = round((submission.score / submission.total * 100)) if submission.total > 0 else 0
    is_passed = percentage >= 50
    
    context = {
        'submission': submission,
        'course': course,
        'score': int(submission.score),
        'total': int(submission.total),
        'percentage': percentage,
        'is_passed': is_passed,
        'exam_results': exam_results,
    }
    return render(request, 'onlinecourseapp/exam_result.html', context)
