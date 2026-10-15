
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Ticket, Comment


class ServiceModelTests(TestCase):

    # Create sample data before each test
    def setUp(self):
        self.user = User.objects.create_user(
            username='testemployee',
            password='testpass123'
        )

        self.support_user = User.objects.create_user(
            username='supportstaff',
            password='testpass123',
            is_staff=True
        )

        self.category = Category.objects.create(
            name='Hardware'
        )

        self.ticket = Ticket.objects.create(
            created_by=self.user,
            title='Laptop keyboard not working',
            description='Keyboard keys are not responding',
            category=self.category
        )

        self.comment = Comment.objects.create(
            ticket=self.ticket,
            user=self.user,
            content='I am checking this issue.'
        )

    # Test whether the category displays its name
    def test_category_string_representation(self):
        self.assertEqual(str(self.category), 'Hardware')

    # Test whether the ticket displays its title
    def test_ticket_string_representation(self):
        self.assertEqual(
            str(self.ticket),
            'Laptop keyboard not working'
        )

    # Test the default ticket status and priority
    def test_ticket_default_values(self):
        self.assertEqual(self.ticket.status, 'Open')
        self.assertEqual(self.ticket.priority, 'Medium')

    # Test whether a new ticket is unassigned
    def test_ticket_is_unassigned_initially(self):
        self.assertIsNone(self.ticket.assigned_to)

    # Test whether a ticket can be assigned to support staff
    def test_ticket_assignment(self):
        self.ticket.assigned_to = self.support_user
        self.ticket.save()

        self.ticket.refresh_from_db()

        self.assertEqual(
            self.ticket.assigned_to,
            self.support_user
        )

    # Test whether the comment displays the author's username
    def test_comment_string_representation(self):
        self.assertEqual(
            str(self.comment),
            'Comment by testemployee'
        )
    # Test the website views
class ServiceViewTests(TestCase):

    # Check whether the Home page opens successfully
    def test_home_page_loads(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'service/home.html')

 # Check whether the Login page opens successfully
    def test_login_page_loads(self):
        response = self.client.get('/login/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'service/login.html')

        # Test login with correct username and password
    def test_login_with_valid_credentials(self):
        # Create a test user
        User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        # Submit the login form
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })

        # Check whether login redirects to the Home page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
    
        # Test login with incorrect credentials
    def test_login_with_invalid_credentials(self):
        response = self.client.post('/login/', {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })

        # Login should fail and display an error
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'Invalid username or password'
        )

        # Test whether a logged-in employee can create a ticket
    def test_create_ticket_with_authenticated_user(self):
        # Create a test employee
        user = User.objects.create_user(
            username='ticketcreator',
            password='testpass123'
        )

        # Create a category for the ticket
        category = Category.objects.create(
            name='Software'
        )

        # Log in the employee
        self.client.login(
            username='ticketcreator',
            password='testpass123'
        )

        # Submit the ticket form
        response = self.client.post('/create-ticket/', {
            'title': 'Printer is not working',
            'description': 'The printer is not printing documents.',
            'category': category.id,
            'priority': 'High'
        })

        # Check whether the request redirects to Home
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        # Check whether the ticket was saved for this employee
        ticket = Ticket.objects.get(
            title='Printer is not working'
        )
        self.assertEqual(ticket.created_by, user)
        self.assertEqual(ticket.priority, 'High')
        
        
        # Test that an anonymous user must log in before creating a ticket
    
    def test_create_ticket_requires_login(self):
        response = self.client.get('/create-ticket/')

        self.assertEqual(response.status_code, 302) 

        # Test that a normal employee cannot access the Support Dashboard
    def test_non_staff_cannot_access_support_dashboard(self):
        # Create a normal employee
        User.objects.create_user(
            username='normalemployee',
            password='testpass123'
        )

        # Log in as the normal employee
        self.client.login(
            username='normalemployee',
            password='testpass123'
        )

        # Try to open the Support Dashboard
        response = self.client.get('/support-dashboard/')

        # The employee should be redirected to Home
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        # Test that support staff can access the Support Dashboard
    def test_staff_can_access_support_dashboard(self):
        # Create a support staff user
        User.objects.create_user(
            username='supportstafftest',
            password='testpass123',
            is_staff=True
        )

        # Log in as support staff
        self.client.login(
            username='supportstafftest',
            password='testpass123'
        )

        # Open the Support Dashboard
        response = self.client.get('/support-dashboard/')

        # Check that the dashboard loads successfully
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'service/support_dashboard.html'
        ) 

        # Test that an employee cannot view another employee's ticket
    def test_employee_cannot_view_another_users_ticket(self):
        # Create the ticket owner
        owner = User.objects.create_user(
            username='ticketowner',
            password='testpass123'
        )

        # Create another employee
        other_user = User.objects.create_user(
            username='otheremployee',
            password='testpass123'
        )

        # Create a category
        category = Category.objects.create(name='Hardware')

        # Create a ticket belonging to the first employee
        ticket = Ticket.objects.create(
            created_by=owner,
            title='Private employee ticket',
            description='Test ticket privacy',
            category=category
        )

        # Log in as the other employee
        self.client.login(
            username='otheremployee',
            password='testpass123'
        )

        # Try to view the ticket
        response = self.client.get(f'/ticket/{ticket.id}/')

        # The employee should be redirected to Home
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
    

        # Test that an employee can view their own ticket
    def test_employee_can_view_own_ticket(self):
        # Create the employee
        user = User.objects.create_user(
            username='ownertest',
            password='testpass123'
        )

        # Create a category
        category = Category.objects.create(
            name='Hardware'
        )

        # Create a ticket belonging to this employee
        ticket = Ticket.objects.create(
            created_by=user,
            title='My laptop issue',
            description='My laptop is not starting',
            category=category
        )

        # Log in as the ticket owner
        self.client.login(
            username='ownertest',
            password='testpass123'
        )

        # Open the employee's own ticket
        response = self.client.get(f'/ticket/{ticket.id}/')

        # Check that the ticket details page loads
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'service/ticket_detail.html'
        )

        # Test that employees see only their own tickets
    def test_my_tickets_shows_only_logged_in_users_tickets(self):
        # Create two employees
        user1 = User.objects.create_user(
            username='employeeone',
            password='testpass123'
        )

        user2 = User.objects.create_user(
            username='employeetwo',
            password='testpass123'
        )

        # Create a category
        category = Category.objects.create(name='Software')

        # Create one ticket for each employee
        own_ticket = Ticket.objects.create(
            created_by=user1,
            title='My software issue',
            description='My application is not opening',
            category=category
        )

        other_ticket = Ticket.objects.create(
            created_by=user2,
            title='Other employee issue',
            description='Another application issue',
            category=category
        )

        # Log in as the first employee
        self.client.login(
            username='employeeone',
            password='testpass123'
        )

        # Open My Tickets
        response = self.client.get('/my-tickets/')

        # Check that the page loads successfully
        self.assertEqual(response.status_code, 200)

        # Check that only this employee's ticket is displayed
        tickets = list(response.context['tickets'])
        self.assertIn(own_ticket, tickets)
        self.assertNotIn(other_ticket, tickets)

        # Test that login is required to access My Tickets
    def test_my_tickets_requires_login(self):
        # Try to access My Tickets without logging in
        response = self.client.get('/my-tickets/')

        # The user should be redirected to login
        self.assertEqual(response.status_code, 302)

        # Test that an employee can add a comment to their own ticket
    def test_employee_can_add_comment_to_own_ticket(self):
        # Create an employee
        user = User.objects.create_user(
            username='commentuser',
            password='testpass123'
        )

        # Create a category
        category = Category.objects.create(name='Software')

        # Create a ticket owned by the employee
        ticket = Ticket.objects.create(
            created_by=user,
            title='Application not opening',
            description='The application closes when opened.',
            category=category
        )

        # Log in as the ticket owner
        self.client.login(
            username='commentuser',
            password='testpass123'
        )

        # Submit a comment
        response = self.client.post(
            f'/ticket/{ticket.id}/',
            {'content': 'I am still experiencing this issue.'}
        )

        # Check that the comment submission redirects back to the ticket
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/ticket/{ticket.id}/')

        # Check that the comment was saved
        self.assertTrue(
            Comment.objects.filter(
                ticket=ticket,
                user=user,
                content='I am still experiencing this issue.'
            ).exists()
        )
    

        # Test search and priority filtering on the Support Dashboard
    def test_support_dashboard_search_and_priority_filter(self):
        # Create a support staff user
        staff_user = User.objects.create_user(
            username='dashboardstaff',
            password='testpass123',
            is_staff=True
        )

        # Create a category
        category = Category.objects.create(name='Hardware')

        # Create two tickets with different titles and priorities
        high_ticket = Ticket.objects.create(
            created_by=staff_user,
            title='Printer not working',
            description='The printer is not responding.',
            category=category,
            priority='High'
        )

        low_ticket = Ticket.objects.create(
            created_by=staff_user,
            title='Keyboard issue',
            description='Some keys are not working.',
            category=category,
            priority='Low'
        )

        # Log in as support staff
        self.client.login(
            username='dashboardstaff',
            password='testpass123'
        )

        # Search for a ticket by title
        response = self.client.get(
            '/support-dashboard/?search=Printer'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context['tickets']),
            [high_ticket]
        )

        # Filter tickets by Low priority
        response = self.client.get(
            '/support-dashboard/?priority=Low'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context['tickets']),
            [low_ticket]
        )

        # Test search and priority filtering on the Support Dashboard
    def test_support_dashboard_search_and_priority_filter(self):
        # Create a support staff user
        staff_user = User.objects.create_user(
            username='dashboardstaff',
            password='testpass123',
            is_staff=True
        )

        # Create a category
        category = Category.objects.create(name='Hardware')

        # Create two tickets with different titles and priorities
        high_ticket = Ticket.objects.create(
            created_by=staff_user,
            title='Printer not working',
            description='The printer is not responding.',
            category=category,
            priority='High'
        )

        low_ticket = Ticket.objects.create(
            created_by=staff_user,
            title='Keyboard issue',
            description='Some keys are not working.',
            category=category,
            priority='Low'
        )

        # Log in as support staff
        self.client.login(
            username='dashboardstaff',
            password='testpass123'
        )

        # Search for a ticket by title
        response = self.client.get(
            '/support-dashboard/?search=Printer'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context['tickets']),
            [high_ticket]
        )

        # Filter tickets by Low priority
        response = self.client.get(
            '/support-dashboard/?priority=Low'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context['tickets']),
            [low_ticket]
        )


        # Test that a ticket cannot be resolved without a resolution message
    def test_ticket_cannot_be_resolved_without_resolution(self):
        # Create a support staff user
        staff_user = User.objects.create_user(
            username='resolutionstaff',
            password='testpass123',
            is_staff=True
        )

        # Create a category
        category = Category.objects.create(name='Hardware')

        # Create a ticket with no resolution message
        ticket = Ticket.objects.create(
            created_by=staff_user,
            title='Laptop not starting',
            description='The laptop does not start.',
            category=category
        )

        # Log in as support staff
        self.client.login(
            username='resolutionstaff',
            password='testpass123'
        )

        # Try to resolve the ticket without a resolution message
        response = self.client.post('/support-dashboard/', {
            'ticket_id': ticket.id,
            'status': 'Resolved'
        })

        # Check that the request redirects to the dashboard
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/support-dashboard/')

        # Check that the ticket remains Open
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, 'Open')

    
    