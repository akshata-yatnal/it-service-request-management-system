from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from .forms import TicketForm
from .forms import *
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request, 'service/home.html')



def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect('/')

        else:
            return render(request,'service/login.html',{'error': 'Invalid username or password'})

    return render(request, 'service/login.html')

def logout_view(request):
    logout(request)
    return redirect('/')



# Protect create_ticket
# @login_required to create_ticket


@login_required

# Create the Create Ticket view
def create_ticket(request):

    if request.method == 'POST':

        form = TicketForm(request.POST)

        if form.is_valid():

            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()

            return redirect('/')

    else:
        form = TicketForm()

    return render(request,'service/create_ticket.html',{'form': form})



# Protect my_tickets

@login_required
# Create the My Tickets view
def my_tickets(request):

    tickets = Ticket.objects.filter(
        created_by=request.user
    )

    return render(request,'service/my_tickets.html',{'tickets': tickets})


# Create the Ticket Details view

# def ticket_detail(request, ticket_id):

#     ticket = Ticket.objects.get(id=ticket_id,created_by=request.user)

#     return render(request,'service/ticket_detail.html',{'ticket': ticket})

# Update the Ticket Details view

@login_required
def ticket_detail(request, ticket_id):
    # Get the ticket by ID
    ticket = Ticket.objects.get(id=ticket_id)

    # Allow the ticket creator or support staff to view it
    if ticket.created_by != request.user and not request.user.is_staff:
         return redirect('/')


    
    comments = Comment.objects.filter(
        ticket=ticket
    )

    if request.method == 'POST':

        form = CommentForm(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.user = request.user
            comment.save()

            return redirect(f'/ticket/{ticket.id}/')

    else:
        form = CommentForm()

    return render(request,'service/ticket_detail.html',{'ticket': ticket,'comments': comments,'form': form,})




# Support Dashboard: Create the dashboard view->where support staff can see all submitted tickets in one place.

@login_required
def support_dashboard(request):
    # Only support staff can access this dashboard
    if not request.user.is_staff:
        return redirect('/')
    
    # Get all tickets
    tickets = Ticket.objects.all()



    # Calculate dashboard statistics
    total_tickets = Ticket.objects.count()
    open_tickets = Ticket.objects.filter(status='Open').count()
    in_progress_tickets = Ticket.objects.filter(status='In Progress').count()
    resolved_tickets = Ticket.objects.filter(status='Resolved').count()
    # Count closed tickets
    closed_tickets = Ticket.objects.filter(status='Closed').count()



    # Get search text entered by support staff
    search = request.GET.get('search', '')

   
    # Get selected status
    status = request.GET.get('status', '')

    # Get selected priority
    priority = request.GET.get('priority', '')

    # Filter tickets by title if search text is entered
    if search:
        tickets = tickets.filter(title__icontains=search)

    # Filter tickets by status if a status is selected
    if status:
        tickets = tickets.filter(status=status)

    # Filter tickets by priority if a priority is selected
    if priority:
        tickets = tickets.filter(priority=priority)


    # Get only support staff for ticket assignment
    users = User.objects.filter(is_staff=True)

    if request.method == 'POST':

        ticket_id = request.POST.get('ticket_id')

        ticket = Ticket.objects.get(id=ticket_id)

        if 'assigned_to' in request.POST:

            form = TicketAssignmentForm(
                request.POST,
                instance=ticket
            )

        elif 'status' in request.POST:
             # Check whether the ticket is being marked as Resolved
            if request.POST.get('status') == 'Resolved' and not (ticket.resolution or '').strip():                 # Show an error when resolution is empty
                messages.error(request, 'Please add a resolution message before resolving the ticket.')
                # Do not allow resolution without a resolution message
                return redirect('/support-dashboard/')
            

            form = TicketStatusForm(request.POST,instance=ticket)

        elif 'resolution' in request.POST:
            form = TicketResolutionForm(request.POST,instance=ticket)    

        if form.is_valid():
            form.save()
             # Show a success message after saving
            messages.success(request, 'Ticket updated successfully.')

            return redirect('/support-dashboard/')

    
    return render(request, 'service/support_dashboard.html',
        {
            'tickets': tickets,
            'users': users,

            # Dashboard statistics
            'total_tickets': total_tickets,
            'open_tickets': open_tickets,
            'in_progress_tickets': in_progress_tickets,
            'resolved_tickets': resolved_tickets,
            'closed_tickets': closed_tickets,
        }
    )

