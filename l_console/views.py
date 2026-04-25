from django.shortcuts import render, redirect,get_object_or_404
from . models import lms_con,category_course,Sub_Category_Course
from .forms import LmsForms
from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime
import json
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
def show_all_lms(request):
    courses = lms_con.objects.all()
    page_num = request.GET.get('page')  # Creating the Total Page
    paginator = Paginator(courses, 2)  # Setting total number of products in a page : 3

    try:
        courses = paginator.page(page_num)  #
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    context = {
        'courses':courses
    }
    return render(request,'showall.html',context)


def course_detail(request, pk):
    course = lms_con.objects.get(pk=pk)
    return render(request, 'course_details.html', {'course': course})

def add_course(request):
    form=LmsForms()
    if request.method=='POST':
        form=LmsForms(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('show_all_lms')
    return render(request,'add_forms.html',{'form':form})


def update_course(request,pk):
    doctor = lms_con.objects.get(course_id=pk)
    form=LmsForms(instance=doctor)
    if request.method=='POST':
        form=LmsForms(request.POST,request.FILES,instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('show_all_lms')
    return render(request,'update_details.html',{'form':form})

def delete_course(request,pk):
    doctor = lms_con.objects.get(course_id=pk)
    doctor.delete()
    return redirect('show_all_lms')


def course_list(request):
    courses = lms_con.objects.all()
    categories_courses = category_course.objects.all()
    sub_categories_courses = Sub_Category_Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses,'categories_courses': categories_courses,
        'sub_categories_courses': sub_categories_courses})

@login_required(login_url='accounts/login')
def course_details_json(request, course_id):
    try:
        course = get_object_or_404(lms_con, course_id=course_id)
        data = {
            'course_id': course.course_id,
            'course_code': course.course_code,
            'model_name': course.model_name,
            'image': course.image.url if course.image else '',
            'course_title': course.course_title,
            'course_short_description': course.course_short_description,
            'course_detailed_description': course.course_detailed_description,
            'course_category': course.category_course.name if course.category_course else '',
            'course_sub_category': course.sub_category_course.name if course.sub_category_course else '',
            'course_type': course.course_type,
            'course_level': course.course_level,
            'course_duration': course.course_duration,
            'number_of_modules': course.number_of_modules,
            'number_of_lessons': course.number_of_lessons,
            'module_title': course.module_title,
            'lesson_title': course.lesson_title,
            'content_type': course.content_type,
            'content_url_upload': course.content_url_upload.url if course.content_url_upload else '',
            'preview_enabled': course.preview_enabled,
            'enrollment_type': course.enrollment_type,
            'enrollment_start_date': course.enrollment_start_date.isoformat() if course.enrollment_start_date else '',
            'enrollment_end_date': course.enrollment_end_date.isoformat() if course.enrollment_end_date else '',
            'access_duration': course.access_duration,
            'prerequisite_courses': course.prerequisite_courses,
            'user_roles_allowed': course.user_roles_allowed,
            'course_price': course.course_price,
            'discount_type_value': course.discount_type_value,
            'tax_applicable': course.tax_applicable,
            'certificate_available': course.certificate_available,
            'certificate_template': course.certificate_template.url if course.certificate_template else '',
            'minimum_completion_percentage': course.minimum_completion_percentage,
        }
        return JsonResponse(data)
    except lms_con.DoesNotExist:
        return JsonResponse({'error': 'Course not found'}, status=404)

@login_required(login_url='accounts/login')
def edit_course(request, course_id):
    course = get_object_or_404(lms_con, course_id=course_id)

    if request.method == 'POST':
        try:
            # Basic Information
            course.course_code = request.POST.get('course_code')
            course.model_name = request.POST.get('model_name')
            course.course_title = request.POST.get('course_title')
            course.course_short_description = request.POST.get('course_short_description')
            course.course_detailed_description = request.POST.get('course_detailed_description')
            category_id = request.POST.get('category_course')
            if category_id:
                course.category_course = category_course.objects.get(id=category_id)
            category_id = request.POST.get('sub_category_course')
            if category_id:
                course.sub_category_course = Sub_Category_Course.objects.get(id=category_id)
            course.course_type = request.POST.get('course_type')
            course.course_level = request.POST.get('course_level')
            course.course_duration = request.POST.get('course_duration')

            # Module & Lesson Information
            course.number_of_modules = request.POST.get('number_of_modules') or None
            course.number_of_lessons = request.POST.get('number_of_lessons') or None
            course.module_title = request.POST.get('module_title')
            course.lesson_title = request.POST.get('lesson_title')
            course.content_type = request.POST.get('content_type')
            course.preview_enabled = request.POST.get('preview_enabled') == 'on'

            # Enrollment Settings
            course.enrollment_type = request.POST.get('enrollment_type')
            course.enrollment_start_date = request.POST.get('enrollment_start_date') or None
            course.enrollment_end_date = request.POST.get('enrollment_end_date') or None
            course.access_duration = request.POST.get('access_duration')
            course.prerequisite_courses = request.POST.get('prerequisite_courses', '')
            course.user_roles_allowed = request.POST.get('user_roles_allowed')

            # Pricing
            course.course_price = request.POST.get('course_price') or None
            course.discount_type_value = request.POST.get('discount_type_value', '')
            course.tax_applicable = request.POST.get('tax_applicable') == 'on'

            # Certification
            course.certificate_available = request.POST.get('certificate_available') == 'on'
            course.minimum_completion_percentage = request.POST.get('minimum_completion_percentage') or None

            # File uploads
            if 'image' in request.FILES:
                course.image = request.FILES['image']
            if 'content_url_upload' in request.FILES:
                course.content_url_upload = request.FILES['content_url_upload']
            if 'certificate_template' in request.FILES:
                course.certificate_template = request.FILES['certificate_template']

            course.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('course_list')

        except Exception as e:
            messages.error(request, f'Error updating course: {str(e)}')

    return redirect('course_list')

@login_required(login_url='accounts/login')
def delete_course1(request, course_id):
    course = get_object_or_404(lms_con, course_id=course_id)

    if request.method == 'POST':
        try:
            course.delete()
            messages.success(request, 'Course deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting course: {str(e)}')

    return redirect('course_list')

@login_required(login_url='accounts/login')
def add_courses(request):
    if request.method == 'POST':
        try:
            # Create a new lms_con instance
            course = lms_con()

            # Basic Information
            course.model_name = request.POST.get('model_name')
            course.course_code = request.POST.get('course_code')
            course.course_title = request.POST.get('course_title')

            # Handle image upload
            if 'image' in request.FILES:
                course.image = request.FILES['image']

            # Description
            course.course_short_description = request.POST.get('course_short_description')
            course.course_detailed_description = request.POST.get('course_detailed_description')

            # Category
            # Category Fix
            category_id = request.POST.get('category_course')
            if category_id:
                course.category_course = category_course.objects.get(id=category_id)

            sub_category_id = request.POST.get('sub_category_course')
            if sub_category_id:
                course.sub_category_course = Sub_Category_Course.objects.get(id=sub_category_id)
            course.course_type = request.POST.get('course_type')
            course.course_level = request.POST.get('course_level')
            course.course_duration = request.POST.get('course_duration')

            # Module Information
            num_modules = request.POST.get('number_of_modules')
            course.number_of_modules = int(num_modules) if num_modules and num_modules.strip() else None

            num_lessons = request.POST.get('number_of_lessons')
            course.number_of_lessons = int(num_lessons) if num_lessons and num_lessons.strip() else None

            course.module_title = request.POST.get('module_title')
            course.lesson_title = request.POST.get('lesson_title')

            # Content Information
            course.content_type = request.POST.get('content_type')

            if 'content_url_upload' in request.FILES:
                course.content_url_upload = request.FILES['content_url_upload']

            # Preview Enabled
            preview_val = request.POST.get('preview_enabled')
            course.preview_enabled = True if preview_val == 'True' else False

            # Enrollment Settings
            course.enrollment_type = request.POST.get('enrollment_type')

            start_date = request.POST.get('enrollment_start_date')
            if start_date and start_date.strip():
                course.enrollment_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

            end_date = request.POST.get('enrollment_end_date')
            if end_date and end_date.strip():
                course.enrollment_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            course.access_duration = request.POST.get('access_duration')
            course.prerequisite_courses = request.POST.get('prerequisite_courses')
            course.user_roles_allowed = request.POST.get('user_roles_allowed')

            # Pricing
            price = request.POST.get('course_price')
            course.course_price = float(price) if price and price.strip() else None

            course.discount_type_value = request.POST.get('discount_type_value')

            tax_val = request.POST.get('tax_applicable')
            course.tax_applicable = True if tax_val == '1' else False

            # Certification
            cert_val = request.POST.get('certificate_available')
            course.certificate_available = True if cert_val == '1' else False

            completion = request.POST.get('minimum_completion_percentage')
            course.minimum_completion_percentage = float(completion) if completion and completion.strip() else None

            if 'certificate_template' in request.FILES:
                course.certificate_template = request.FILES['certificate_template']

            # Save to database
            course.save()
            messages.success(request, '✅ Course added successfully!')

            return redirect('course_list')

        except Exception as e:
            messages.error(request, f'❌ Error adding course: {str(e)}')
            return redirect('course_list')

    # If not POST, render the add course page
    return render(request, 'addforms.html')

@login_required(login_url='accounts/login')
def searchBar(request):
    if request.method == 'GET':  # get = Get => True
        query = request.GET.get('query')  # query = 999, ABC, ABC99, ABC99$#$#
        if query:  # True
            cs = lms_con.objects.filter(course_title__icontains=query)  # 999 = 4 records found
            return render(request, 'searchbar.html', {"cs": cs})
        else:
            print("No Products Found to show in the Database")
            return render(request, 'searchbar.html', {})