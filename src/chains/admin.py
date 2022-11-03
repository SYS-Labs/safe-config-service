from typing import List, Optional

from django.contrib import admin
from django.db.models import Model
from django.http import HttpRequest

from .models import Chain, Feature, GasPrice, Wallet


class GasPriceInline(admin.TabularInline[Model, Model]):
    model = GasPrice
    extra = 0
    verbose_name_plural = "Gas prices set for this chain"


class FeatureInline(admin.TabularInline[Model, Model]):
    model = Feature.chains.through
    extra = 0
    verbose_name_plural = "Features enabled for this chain"


class WalletInline(admin.TabularInline[Model, Model]):
    model = Wallet.chains.through
    extra = 0
    verbose_name_plural = "Wallets enabled for this chain"


@admin.register(Chain)
class ChainAdmin(admin.ModelAdmin[Chain]):
    list_display = (
        "id",
        "name",
        "rpc_uri",
        "safe_apps_rpc_uri",
        "relevance",
    )
    search_fields = ("name", "id")
    ordering = (
        "relevance",
        "name",
    )
    inlines = [FeatureInline, GasPriceInline, WalletInline]

    def get_readonly_fields(
        self, request: HttpRequest, obj: Optional[Chain] = None
    ) -> List[str]:
        if (
            request.user.has_perm("chains.change_only_warning")
            and not request.user.is_superuser
        ):
            readonly_fields = [f.name for f in self.model._meta.fields]
            readonly_fields.remove("warning")
            return readonly_fields
        return []


@admin.register(GasPrice)
class GasPriceAdmin(admin.ModelAdmin[GasPrice]):
    list_display = (
        "chain_id",
        "oracle_uri",
        "fixed_wei_value",
        "rank",
    )
    search_fields = ("chain_id", "oracle_uri")
    ordering = ("rank",)


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin[Wallet]):
    list_display = ("key",)


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin[Feature]):
    list_display = ("key",)
