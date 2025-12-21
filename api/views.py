from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from book.models import UserProfile, Task
from .serializers import UserSerializer, TaskSerializer 
from django.utils import timezone
from datetime import datetime

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def main(request):
    return Response({"message": f"Hello, {request.user.username}!"})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def set_task(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=profile)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_task(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    date_str = request.query_params.get('date')
    tasks = Task.objects.filter(user=profile).order_by('-date')
    
    if date_str:
        try:
            filter_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            tasks = tasks.filter(date__date=filter_date)
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data, status=200)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def edit_task(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    task_id = request.data.get('id')
    if not task_id:
        return Response({"error": "Task ID is required"}, status=400)
    
    task = get_object_or_404(Task, id=task_id, user=profile)
    serializer = TaskSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def summary(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    tasks = Task.objects.filter(user=profile)
    
    total_entries = tasks.count()
    total_paid = tasks.filter(payment_status=True).count()
    total_unpaid = tasks.filter(payment_status=False).count()
    
    total_seconds = 0
    total_earnings = 0
    
    for task in tasks:
        # Calculate duration
        task_date = task.date.date()
        start_dt = datetime.combine(task_date, task.start)
        end_dt = datetime.combine(task_date, task.end)
        
        if end_dt < start_dt:
            from datetime import timedelta
            end_dt += timedelta(days=1)
            
        duration = end_dt - start_dt

        net_seconds = max(0, duration.total_seconds() - (task.break_duration * 60))
        total_seconds += net_seconds
        

        task_hours = net_seconds / 3600
        total_earnings += float(task.hourly_rate) * task_hours
    
    total_hours = round(total_seconds / 3600, 2)
    
    data = {
        "total_entries": total_entries,
        "total_hours": total_hours,
        "total_earnings": round(total_earnings, 2),
        "total_paid": total_paid,
        "total_unpaid": total_unpaid
    }
    return Response(data, status=200)
