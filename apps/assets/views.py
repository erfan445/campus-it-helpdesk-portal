from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from apps.common import paginate_queryset
from .forms import AssetForm
from .models import Asset


@login_required
def asset_list(request):
    assets = Asset.objects.select_related('assigned_to')
    query = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()
    category = request.GET.get('category', '').strip()

    if query:
        assets = assets.filter(
            Q(asset_tag__icontains=query)
            | Q(name__icontains=query)
            | Q(serial_number__icontains=query)
            | Q(location__icontains=query)
            | Q(assigned_to__username__icontains=query)
        )
    if status:
        assets = assets.filter(status=status)
    if category:
        assets = assets.filter(category=category)

    page_obj = paginate_queryset(request, assets, per_page=10)

    return render(request, 'assets/asset_list.html', {
        'page_obj': page_obj,
        'status_choices': Asset.Status.choices,
        'category_choices': Asset.Category.choices,
        'selected': {'q': query, 'status': status, 'category': category},
    })


@login_required
def asset_detail(request, asset_id):
    asset = get_object_or_404(Asset.objects.select_related('assigned_to'), id=asset_id)
    return render(request, 'assets/asset_detail.html', {'asset': asset})


@login_required
def asset_create(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            asset = form.save()
            messages.success(request, f'Asset {asset.asset_tag} was added.')
            return redirect('asset_detail', asset_id=asset.id)
    else:
        form = AssetForm()
    return render(request, 'assets/asset_form.html', {'form': form, 'page_title': 'Add Asset'})


@login_required
def asset_update(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Asset updated.')
            return redirect('asset_detail', asset_id=asset.id)
    else:
        form = AssetForm(instance=asset)
    return render(request, 'assets/asset_form.html', {'form': form, 'page_title': 'Update Asset'})
