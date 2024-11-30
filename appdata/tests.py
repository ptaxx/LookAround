from django.test import TestCase
from .models import CustomUser, Game, Area, Team, Venue
from datetime import time
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile



        
        
class TeamModelCRUDTestCase(TestCase):
    def setUp(self):
        # Create a CustomUser instance to use as a moderator
        self.moderator = CustomUser.objects.create_user(
            username="moderator1",
            email="moderator1@example.com",
            password="password123"
        )
        
        # Create another CustomUser instance to use as a team member
        self.team_user = CustomUser.objects.create_user(
            username="teamuser1",
            email="teamuser1@example.com",
            password="password123"
        )
        
        # Create a Team instance
        self.team = Team.objects.create(
            name="Test Team",
            moderator=self.moderator
        )
        self.team.team_user.add(self.team_user)

    def test_team_creation(self):
        self.assertEqual(Team.objects.count(), 1)
        self.assertEqual(self.team.name, "Test Team")
        self.assertEqual(self.team.moderator, self.moderator)
        self.assertIn(self.team_user, self.team.team_user.all())

    def test_team_read(self):
        team = Team.objects.get(id=self.team.id)
        self.assertEqual(team.name, "Test Team")
        self.assertEqual(team.moderator.username, "moderator1")
        self.assertIn(self.team_user, team.team_user.all())

    def test_team_update(self):
        # Update team name
        self.team.name = "Updated Team Name"
        self.team.save()
        updated_team = Team.objects.get(id=self.team.id)
        self.assertEqual(updated_team.name, "Updated Team Name")
        
        # Add another team member
        new_user = CustomUser.objects.create_user(
            username="teamuser2",
            email="teamuser2@example.com",
            password="password123"
        )
        self.team.team_user.add(new_user)
        self.assertIn(new_user, self.team.team_user.all())

    def test_team_delete(self):
        self.team.delete()
        self.assertEqual(Team.objects.count(), 0)
        
        
class VenueModelCRUDTestCase(TestCase):

    def setUp(self):
        # Create instances of related models
        self.area = Area.objects.create(name="Test Area", description="A test area", weather_id="123456")
        self.user = CustomUser.objects.create_user(username="user1", email="user1@example.com", password="password123")
        
        # Create a Venue instance
        self.venue = Venue.objects.create(
            name="Test Venue",
            area=self.area,
            opening_hour=time(9, 0),  # 9:00 AM
            closing_hour=time(18, 0),  # 6:00 PM
            description="A test venue for events and activities",
            contact=self.user,
            tripadvisor_link="https://www.tripadvisor.com/TestVenue"
        )

    def test_venue_creation(self):
        # Ensure the venue is created correctly
        self.assertEqual(Venue.objects.count(), 1)
        venue = Venue.objects.first()
        self.assertEqual(venue.name, "Test Venue")
        self.assertEqual(venue.area, self.area)
        self.assertEqual(venue.opening_hour, time(9, 0))
        self.assertEqual(venue.closing_hour, time(18, 0))
        self.assertEqual(venue.description, "A test venue for events and activities")
        self.assertEqual(venue.contact, self.user)
        self.assertEqual(venue.tripadvisor_link, "https://www.tripadvisor.com/TestVenue")

    def test_venue_read(self):
        # Ensure we can retrieve the venue and check its fields
        venue = Venue.objects.get(id=self.venue.id)
        self.assertEqual(venue.name, "Test Venue")
        self.assertEqual(venue.area, self.area)
        self.assertEqual(venue.opening_hour, time(9, 0))
        self.assertEqual(venue.closing_hour, time(18, 0))
        self.assertEqual(venue.description, "A test venue for events and activities")
        self.assertEqual(venue.contact, self.user)
        self.assertEqual(venue.tripadvisor_link, "https://www.tripadvisor.com/TestVenue")

    def test_venue_update(self):
        # Update the venue's description and save
        self.venue.description = "Updated venue description"
        self.venue.save()

        updated_venue = Venue.objects.get(id=self.venue.id)
        self.assertEqual(updated_venue.description, "Updated venue description")

    def test_venue_delete(self):
        # Ensure the venue is deleted
        venue_id = self.venue.id
        self.venue.delete()
        with self.assertRaises(Venue.DoesNotExist):
            Venue.objects.get(id=venue_id)

    def test_related_fields(self):
        # Ensure related fields are correctly linked
        venue = Venue.objects.get(id=self.venue.id)

        # Check the area
        self.assertEqual(venue.area, self.area)

        # Check the contact user
        self.assertEqual(venue.contact, self.user)

        # Check the TripAdvisor link
        self.assertEqual(venue.tripadvisor_link, "https://www.tripadvisor.com/TestVenue")


class CustomUserTestCase(TestCase):
    def setUp(self):
        # Create a dummy Area instance
        self.area = Area.objects.create(name="Test Area", description="A test area")
        
    def test_create_custom_user(self):
        user = get_user_model().objects.create_user(
            username='testuser',
            password='password123',
            short_bio='This is a test user',
            isplayer=True,
            current_area=self.area,
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.short_bio, 'This is a test user')
        self.assertTrue(user.isplayer)
        self.assertEqual(user.current_area, self.area)
        self.assertTrue(user.check_password('password123'))

    def test_read_custom_user(self):
        user = get_user_model().objects.create_user(
            username='testuser',
            password='password123',
            short_bio='This is a test user',
            isplayer=True,
            current_area=self.area,
        )
        fetched_user = get_user_model().objects.get(username='testuser')
        self.assertEqual(fetched_user.username, 'testuser')
        self.assertEqual(fetched_user.short_bio, 'This is a test user')
        self.assertEqual(fetched_user.current_area, self.area)

    def test_update_custom_user(self):
        user = get_user_model().objects.create_user(
            username='testuser',
            password='password123',
            short_bio='This is a test user',
            isplayer=True,
            current_area=self.area,
        )
        user.short_bio = 'Updated bio'
        user.save()
        
        updated_user = get_user_model().objects.get(username='testuser')
        self.assertEqual(updated_user.short_bio, 'Updated bio')

    def test_delete_custom_user(self):
        user = get_user_model().objects.create_user(
            username='testuser',
            password='password123',
            short_bio='This is a test user',
            isplayer=True,
            current_area=self.area,
        )
        user.delete()
        
        with self.assertRaises(get_user_model().DoesNotExist):
            get_user_model().objects.get(username='testuser')

    def test_userpic_upload(self):
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        
        user = get_user_model().objects.create_user(
            username='testuser',
            password='password123',
            short_bio='This is a test user',
            isplayer=True,
            current_area=self.area,
            userpic=image
        )
        
        self.assertTrue(user.userpic.name.startswith('static/profile_pictures/'))       
        
