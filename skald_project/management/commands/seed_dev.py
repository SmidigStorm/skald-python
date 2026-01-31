"""Seed the development database with test data."""

from django.core.management.base import BaseCommand

from knowledge.models import Capability, Domain, SubDomain
from users.models import Product, ProductMembership, User


class Command(BaseCommand):
    help = "Seed the development database with test data"

    def handle(self, *args, **options):
        self.stdout.write("Seeding development database...")

        # Create users
        self.stdout.write("Creating users...")
        admin = self._create_user("admin", is_superuser=True, is_staff=True)
        alice = self._create_user("alice", is_staff=True)
        bob = self._create_user("bob", is_staff=True)
        charlie = self._create_user("charlie", is_staff=True)

        # Create products
        self.stdout.write("Creating products...")
        skald = self._create_product("Skald", "AI-native product development platform")
        acme = self._create_product("Acme App", "Example project for testing")

        # Create memberships
        self.stdout.write("Creating memberships...")
        self._create_membership(alice, skald, ProductMembership.Role.MANAGER)
        self._create_membership(bob, skald, ProductMembership.Role.CONTRIBUTOR)
        self._create_membership(charlie, skald, ProductMembership.Role.VIEWER)
        self._create_membership(alice, acme, ProductMembership.Role.MANAGER)

        # Create domain hierarchy for Skald
        self.stdout.write("Creating domain hierarchy for Skald...")

        # User Access domain
        user_access = self._create_domain(skald, "User Access", "Authentication, authorization, and user management")
        auth = self._create_subdomain(user_access, "Authentication", "Login, logout, and session management")
        self._create_capability(auth, "Login", "User login with username and password")
        self._create_capability(auth, "Logout", "User logout and session termination")
        self._create_capability(auth, "Password Reset", "Reset forgotten password via email")

        authz = self._create_subdomain(user_access, "Authorization", "Role-based access control")
        self._create_capability(authz, "Role Assignment", "Assign users to products with roles")
        self._create_capability(authz, "Permission Check", "Verify user has permission for action")

        # Domain Knowledge domain
        domain_knowledge = self._create_domain(skald, "Domain Knowledge", "Domain modeling and ubiquitous language")
        modeling = self._create_subdomain(domain_knowledge, "Modeling", "Entity and relationship modeling")
        self._create_capability(modeling, "Manage Domains", "Create, update, delete domains")
        self._create_capability(modeling, "Manage SubDomains", "Create, update, delete subdomains")
        self._create_capability(modeling, "Manage Capabilities", "Create, update, delete capabilities")

        glossary = self._create_subdomain(domain_knowledge, "Glossary", "Ubiquitous language definitions")
        self._create_capability(glossary, "Manage Terms", "Create, update, delete glossary terms")

        # Planning domain
        planning = self._create_domain(skald, "Planning", "Backlog and sprint management")
        backlog = self._create_subdomain(planning, "Backlog", "Product backlog management")
        self._create_capability(backlog, "Prioritize Items", "Order backlog items by priority")
        self._create_capability(backlog, "Estimate Items", "Add effort estimates to items")

        # Create minimal hierarchy for Acme
        self.stdout.write("Creating domain hierarchy for Acme App...")
        core = self._create_domain(acme, "Core", "Core application functionality")
        features = self._create_subdomain(core, "Features", "Main product features")
        self._create_capability(features, "Feature A", "First example feature")
        self._create_capability(features, "Feature B", "Second example feature")

        self.stdout.write(self.style.SUCCESS("✓ Development database seeded successfully!"))
        self.stdout.write("")
        self.stdout.write("Test accounts:")
        self.stdout.write("  admin / admin (superuser)")
        self.stdout.write("  alice / alice (manager of Skald & Acme)")
        self.stdout.write("  bob / bob (contributor on Skald)")
        self.stdout.write("  charlie / charlie (viewer on Skald)")
        self.stdout.write("")
        self.stdout.write(f"Products: {Product.objects.count()}")
        self.stdout.write(f"Domains: {Domain.objects.count()}")
        self.stdout.write(f"SubDomains: {SubDomain.objects.count()}")
        self.stdout.write(f"Capabilities: {Capability.objects.count()}")

    def _create_user(self, username: str, is_superuser: bool = False, is_staff: bool = False) -> User:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": f"{username}@example.com",
                "is_superuser": is_superuser,
                "is_staff": is_staff,
            },
        )
        if created or not user.has_usable_password():
            user.set_password(username)  # password = username for dev
            user.save()
        return user

    def _create_product(self, name: str, description: str) -> Product:
        product, _ = Product.objects.get_or_create(
            name=name,
            defaults={"description": description, "is_active": True},
        )
        return product

    def _create_membership(self, user: User, product: Product, role: str) -> ProductMembership:
        membership, _ = ProductMembership.objects.get_or_create(
            user=user,
            product=product,
            defaults={"role": role},
        )
        return membership

    def _create_domain(self, product: Product, name: str, description: str) -> Domain:
        domain, _ = Domain.objects.get_or_create(
            product=product,
            name=name,
            defaults={"description": description},
        )
        return domain

    def _create_subdomain(self, domain: Domain, name: str, description: str) -> SubDomain:
        subdomain, _ = SubDomain.objects.get_or_create(
            domain=domain,
            name=name,
            defaults={"description": description},
        )
        return subdomain

    def _create_capability(self, subdomain: SubDomain, name: str, description: str) -> Capability:
        capability, _ = Capability.objects.get_or_create(
            subdomain=subdomain,
            name=name,
            defaults={"description": description},
        )
        return capability
