from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView, ListView
from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from .models import CoilIn, CoilPallet, CoilOut, CoilNumber
from django.contrib import messages
from .forms import CoilInForm, CoilPalletForm, CoilNumberFormSet, CoilOutForm, SKUForm

def has_group(user, group_names):
    if user.is_superuser:
        return True
    if isinstance(group_names, str):
        group_names = [group_names]
    return user.groups.filter(name__in=group_names).exists()

def is_sku_manager(user):
    return has_group(user, 'SKU_Manager')

def is_coil_in(user):
    return has_group(user, 'Coil_In')

def is_coil_out(user):
    return has_group(user, ['Coil_Out', 'Coil_In'])

def is_adjuster(user):
    return has_group(user, 'Adjuster')

def is_viewer(user):
    return has_group(user, ['Viewer', 'Coil_In', 'Coil_Out', 'Adjuster', 'SKU_Manager']) or user.is_authenticated

# Create your views here.
def index(request):
    if request.method == 'POST':
        if not is_sku_manager(request.user):
             messages.error(request, 'คุณไม่มีสิทธิ์เพิ่ม SKU')
             return redirect('coil:index')

        form = SKUForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'บันทึก SKU เรียบร้อยแล้ว')
            return redirect('coil:index')  # Redirect to clear POST data
    else:
        form = SKUForm()
        
    return render(request, 'index.html', {'form': form})

@user_passes_test(is_viewer)
def coilin_list(request):
    coils = CoilIn.objects.all().order_by('-timestamp1')
    return render(request, 'coil/coilin_list.html', {'coils': coils})

class CoilInCreateView(UserPassesTestMixin, CreateView):
    model = CoilIn
    form_class = CoilInForm
    template_name = 'coil/coilin_form.html'
    
    def test_func(self):
        return is_coil_in(self.request.user)
    
    def get_success_url(self):
        return reverse('coil:coilin_detail', kwargs={'pk': self.object.pk})

from django.db.models import Sum

class CoilInDetailView(UserPassesTestMixin, DetailView):
    model = CoilIn
    template_name = 'coil/coilin_detail.html'
    context_object_name = 'coil'
    
    def test_func(self):
        return is_viewer(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Calculate total weight of all coils in this lot
        # coil -> coilpallet_set -> coilnumber_set
        total_weight = CoilNumber.objects.filter(coilpallet__coilin=self.object).aggregate(Sum('weight'))['weight__sum']
        context['total_weight'] = total_weight or 0
        return context

@user_passes_test(is_coil_in)
def add_pallet(request, pk, pallet_pk=None):
    """
    Add or edit a pallet.
    - If pallet_pk is None: Create new pallet
    - If pallet_pk is provided: Edit existing pallet
    """
    coil = get_object_or_404(CoilIn, pk=pk)
    pallet = None
    is_edit = False

    if pallet_pk:
        pallet = get_object_or_404(CoilPallet, pk=pallet_pk, coilin=coil)
        is_edit = True

    if request.method == 'POST':
        form = CoilPalletForm(request.POST, instance=pallet)
        formset = CoilNumberFormSet(request.POST, instance=pallet)

        if form.is_valid() and formset.is_valid():
            pallet = form.save(commit=False)
            pallet.coilin = coil
            pallet.save()

            # Save the formset with the pallet as the instance
            instances = formset.save(commit=False)
            for instance in instances:
                instance.coilpallet = pallet
                instance.save()

            # Handle deletions from formset
            for obj in formset.deleted_objects:
                obj.delete()

            return redirect('coil:coilin_detail', pk=coil.pk)
    else:
        form = CoilPalletForm(instance=pallet)
        formset = CoilNumberFormSet(instance=pallet)

    return render(request, 'coil/add_pallet.html', {
        'coil': coil,
        'form': form,
        'formset': formset,
        'is_edit': is_edit,
        'pallet': pallet
    })

@user_passes_test(is_viewer)
def print_labels(request, pk):
    coil = get_object_or_404(CoilIn, pk=pk)
    pallets = coil.coilpallet_set.all()

    # Pre-calculate totals for each pallet
    for pallet in pallets:
        coil_numbers = pallet.coilnumber_set.all()
        pallet.total_weight = sum([c.weight for c in coil_numbers if c.weight])
        pallet.total_count = coil_numbers.count()
        pallet.all_coils = coil_numbers # accessible in template simply

    return render(request, 'coil/print_label.html', {'coil': coil, 'pallets': pallets})

def label_list(request):
    """Display all labels with their coils and pallets"""
    coils = CoilIn.objects.all().order_by('-timestamp2')

    # Pre-calculate pallet info for each coil
    for coil in coils:
        pallets = coil.coilpallet_set.all()
        coil.pallet_count = pallets.count()
        coil.total_coils = sum([p.coilnumber_set.count() for p in pallets])

    return render(request, 'coil/label_list.html', {'coils': coils})

class CoilOutCreateView(UserPassesTestMixin, CreateView):
    model = CoilOut
    form_class = CoilOutForm
    template_name = 'coil/coilout_form.html'

    def test_func(self):
        return is_coil_out(self.request.user)

    def get_success_url(self):
        return reverse('coil:coilout_list')

class CoilOutListView(ListView):
    model = CoilOut
    template_name = 'coil/coilout_list.html'
    context_object_name = 'coilouts'
    ordering = ['-timestamp2']

class CoilOutDetailView(UserPassesTestMixin, DetailView):
    model = CoilOut
    template_name = 'coil/coilout_detail.html'
    context_object_name = 'coilout'
    
    def test_func(self):
        return is_viewer(self.request.user)

# Update and Delete Views

from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy

class CoilInUpdateView(UserPassesTestMixin, UpdateView):
    model = CoilIn
    form_class = CoilInForm
    template_name = 'coil/coilin_form.html'
    
    def test_func(self):
        return is_adjuster(self.request.user)
    
    def get_success_url(self):
        return reverse('coil:coilin_detail', kwargs={'pk': self.object.pk})

class CoilInDeleteView(UserPassesTestMixin, DeleteView):
    model = CoilIn
    template_name = 'coil/confirm_delete.html'
    success_url = reverse_lazy('coil:coilin_list')

    def test_func(self):
        return is_adjuster(self.request.user)

from django.http import JsonResponse
from .models import CoilNumber

@user_passes_test(is_coil_out)
def get_coil_sku(request, pk):
    """API endpoint to get SKU for a coil number (AJAX requests only)"""
    print(f"DEBUG: get_coil_sku called for pk={pk} by user {request.user}")
    try:
        coil_number = CoilNumber.objects.get(pk=pk)
        sku_id = coil_number.coilpallet.type0.id
        # Also return the name for better debugging or if needed
        sku_name = str(coil_number.coilpallet.type0)
        weight = coil_number.weight
        print(f"DEBUG: Found SKU {sku_name} (ID: {sku_id}), Weight: {weight}")
        return JsonResponse({'sku_id': sku_id, 'sku_name': sku_name, 'weight': weight})
    except CoilNumber.DoesNotExist:
        print(f"DEBUG: CoilNumber {pk} not found")
        return JsonResponse({'error': 'Coil not found'}, status=404)
    except Exception as e:
        print(f"DEBUG: Error in get_coil_sku: {e}")
        return JsonResponse({'error': str(e)}, status=500)

class CoilOutUpdateView(UserPassesTestMixin, UpdateView):
    model = CoilOut
    form_class = CoilOutForm
    template_name = 'coil/coilout_form.html'
    
    def test_func(self):
        return is_adjuster(self.request.user)
    
    def get_success_url(self):
        return reverse('coil:coilout_detail', kwargs={'pk': self.object.pk})

class CoilOutDeleteView(UserPassesTestMixin, DeleteView):
    model = CoilOut
    template_name = 'coil/confirm_delete.html'
    success_url = reverse_lazy('coil:coilout_list')
    
    def test_func(self):
        return is_adjuster(self.request.user)
