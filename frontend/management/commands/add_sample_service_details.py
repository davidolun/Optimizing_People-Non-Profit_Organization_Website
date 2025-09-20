from django.core.management.base import BaseCommand
from frontend.models import ServiceDetail


class Command(BaseCommand):
    help = 'Add sample service details to the database'

    def handle(self, *args, **options):
        # Medical & Mental Health Services
        medical_service, created = ServiceDetail.objects.get_or_create(
            service_type='medical',
            defaults={
                'title': 'Medical & Mental Health Services',
                'description': 'Our medical clinics provide comprehensive healthcare services to communities that lack access to proper medical care. We believe that health is a fundamental right, not a privilege.',
                'image_url': 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
                'features': [
                    'Free medical consultations and check-ups',
                    'Basic treatment for common illnesses',
                    'Mental health counseling and support',
                    'Health education and awareness programs',
                    'Emergency medical assistance',
                    'Referral services for specialized care'
                ],
                'order': 1,
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created Medical & Mental Health Services')
            )
        else:
            self.stdout.write('Medical & Mental Health Services already exists')

        # Clean Water Access
        water_service, created = ServiceDetail.objects.get_or_create(
            service_type='water',
            defaults={
                'title': 'Clean Water Access',
                'description': 'Access to clean water is essential for health and development. Our water supply projects ensure communities have reliable access to safe drinking water.',
                'image_url': 'https://images.unsplash.com/photo-1581094794329-c8112a89af12?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
                'features': [
                    'Borehole drilling and installation',
                    'Water treatment and purification systems',
                    'Community water management training',
                    'Maintenance and repair services',
                    'Water quality testing and monitoring',
                    'Emergency water supply during crises'
                ],
                'order': 2,
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created Clean Water Access')
            )
        else:
            self.stdout.write('Clean Water Access already exists')

        # Food Security Programs
        food_service, created = ServiceDetail.objects.get_or_create(
            service_type='food',
            defaults={
                'title': 'Food Security Programs',
                'description': 'We combat hunger and malnutrition through organized food distribution programs, ensuring families have access to nutritious meals.',
                'image_url': 'https://images.unsplash.com/photo-1593113598332-cd288d649433?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
                'features': [
                    'Regular food distribution drives',
                    'Emergency food assistance',
                    'Nutritional education programs',
                    'Community kitchen initiatives',
                    'Agricultural support and training',
                    'School feeding programs'
                ],
                'order': 3,
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created Food Security Programs')
            )
        else:
            self.stdout.write('Food Security Programs already exists')

        self.stdout.write(
            self.style.SUCCESS('Successfully added sample service details!')
        )
