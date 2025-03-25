from rest_framework import status
from rest_framework.response import Response
from .models import *
from .serializers import *
from datetime import datetime, timedelta
from rest_framework.decorators import api_view


@api_view(["GET"])
def list_tasks(request):
    tasks = Task.objects.all().order_by("-created_at")  # Fetch all tasks, ordered by newest first
    if not tasks:
        return Response({"error": "Task not found"}, status=status.HTTP_400_BAD_REQUEST)
    serializer = TaskSerializer(tasks, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_task(request):
    user_id = request.data.get("user_id")
    required_fields = ["user_id", "name", "description"]
    missing_fields = [field for field in required_fields if not request.data.get(field)]
    # Check if required fields are missing
    if missing_fields:
        return Response({"error": f"{', '.join(missing_fields)} is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.filter(id=user_id).last()
    except:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check if user is an admin (role = 0)
    if user.role != 0:
        return Response({"error": "Only admins can create tasks"}, status=status.HTTP_403_FORBIDDEN)

    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(created_by=user)  # Assign the task creator
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def update_task(request, task_id):
    try:
        task = Task.objects.filter(id=task_id).last()
    except:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    user_id = request.data.get("user_id")
    if not user_id:
        return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
    if not task:
        return Response({"error": "Task not found"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(id=user_id)
    except:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Ensure only admin users (role = 0) can update tasks
    if user.role != 0:
        return Response({"error": "Only admins can update tasks"}, status=status.HTTP_403_FORBIDDEN)

    # Allowed fields for update
    allowed_fields = ["name", "description", "task_type"]
    update_data = {key: value for key, value in request.data.items() if key in allowed_fields}

    # Validate task_type if provided
    if "task_type" in update_data and update_data["task_type"] not in dict(Task.TASK_TYPES).keys():
        return Response({"error": f"Invalid task_type. Allowed values: {', '.join(dict(Task.TASK_TYPES).keys())}"},
                        status=status.HTTP_400_BAD_REQUEST)

    # Validate status if provided
    if "status" in update_data and update_data["status"] not in dict(Task.STATUS_CHOICES).keys():
        return Response({"error": f"Invalid status. Allowed values: {', '.join(dict(Task.STATUS_CHOICES).keys())}"},
                        status=status.HTTP_400_BAD_REQUEST)

    # Update the task
    for key, value in update_data.items():
        setattr(task, key, value)
    task.save()

    serializer = TaskSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_normal_users(request):
    # Fetch all normal users (role = 1) as 0 role is for admin and admin is assigning the task to normal_users
    normal_users = User.objects.filter(role=1)
    serializer = UserSerializer(normal_users, many=True)
    users_data = serializer.data
    for user in users_data:
        user.pop("role", None)
    return Response(serializer.data)


@api_view(["GET"])
def get_tasks_for_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    # Fetch tasks assigned to a specific user
    user_tasks = UserTask.objects.filter(user=user).select_related("task").order_by("-weightage")

    if not user_tasks.exists():
        return Response({"error": "No tasks assigned to this user"}, status=status.HTTP_404_NOT_FOUND)

    tasks_data = [
        {
            "task_id": ut.task.id,
            "name": ut.task.name,
            "description": ut.task.description,
            "task_type": ut.task.task_type,
            "weightage": ut.weightage,
            "deadline": ut.deadline.strftime("%Y-%m-%d"),  # Format deadline
        }
        for ut in user_tasks
    ]

    return Response(tasks_data, status=status.HTTP_200_OK)


def is_valid_date(date_str):
    # Check if the date is in YYYY-MM-DD format.
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


@api_view(["POST"])
def assign_task(request):
    """Assign tasks to users with weightage and deadlines(both are optional)."""
    task_ids = request.data.get("task_ids", [])
    user_ids = request.data.get("user_ids", [])
    weightage_data = request.data.get("weightage", {})
    deadline_data = request.data.get("deadline", {})

    if not task_ids or not user_ids:
        return Response({"error": "task_ids and user_ids are required"}, status=status.HTTP_400_BAD_REQUEST)
    if type(task_ids) != list or type(user_ids) != list:  # Ensuring task_ids and user_ids are lists
        return Response({"error": "Please pass task_ids and user_ids in list format"},
                        status=status.HTTP_400_BAD_REQUEST)

    # Validation: Either multiple users OR multiple tasks, but not both
    if len(task_ids) > 1 and len(user_ids) > 1:
        return Response({
            "error": "Only one task can be assigned to multiple users OR a single user can have multiple tasks, not both."},
            status=status.HTTP_400_BAD_REQUEST)
    if deadline_data:  # Validate deadline format if provided
        invalid_dates = {task_id: date for task_id, date in deadline_data.items() if not is_valid_date(date)}

        if invalid_dates:
            return Response(
                {"error": f"Invalid date format for task deadlines: {invalid_dates}. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )
    tasks = Task.objects.filter(id__in=task_ids)
    valid_task_ids = set(tasks.values_list("id", flat=True))
    invalid_task_ids = [tid for tid in task_ids if tid not in valid_task_ids]

    users = User.objects.filter(id__in=user_ids, role=1)
    valid_user_ids = set(users.values_list("id", flat=True))
    invalid_user_ids = [uid for uid in user_ids if uid not in valid_user_ids]
    # Return error if invalid task or user IDs found in the request.data
    if invalid_task_ids:
        return Response({"error": f"Invalid task IDs: {invalid_task_ids}"}, status=status.HTTP_400_BAD_REQUEST)
    if invalid_user_ids:
        return Response({"error": f"Invalid user IDs: {invalid_user_ids}"}, status=status.HTTP_400_BAD_REQUEST)

    assigned_tasks = []
    already_assigned_users = []

    for task in tasks:
        for user in users:
            existing_assignment = UserTask.objects.filter(user=user, task=task).exists()
            if existing_assignment:
                already_assigned_users.append({"user_name": user.name, "task_name": task.name})
                continue  # Skip already assigned users

            user_task, created = UserTask.objects.get_or_create(
                user=user,
                task=task,
                defaults={
                    "weightage": weightage_data.get(str(task.id), 1),
                    "deadline": deadline_data.get(str(task.id), datetime.today() + timedelta(days=10))
                }
            )
            assigned_tasks.append(user_task)

    # Return error if task is already assigned
    if already_assigned_users:
        return Response(
            {"error": "Task is already assigned to the following users", "details": already_assigned_users},
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response(
        {
            "message": f"Successfully assigned {len(tasks)} task(s) to {len(users)} user(s)."
        },
        status=status.HTTP_201_CREATED
    )
