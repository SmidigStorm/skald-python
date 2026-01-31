from django.db import models

from users.models import Product


class Domain(models.Model):
    """Top-level area of concern within a product."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="domains",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["product", "name"]
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class SubDomain(models.Model):
    """Nested area within a domain containing entities, capabilities, and glossary."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    domain = models.ForeignKey(
        Domain,
        on_delete=models.CASCADE,
        related_name="subdomains",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["domain", "name"]
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Capability(models.Model):
    """What the system can do. Verb-like actions at the subdomain level."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    subdomain = models.ForeignKey(
        SubDomain,
        on_delete=models.CASCADE,
        related_name="capabilities",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["subdomain", "name"]
        ordering = ["name"]
        verbose_name_plural = "capabilities"

    def __str__(self) -> str:
        return self.name
