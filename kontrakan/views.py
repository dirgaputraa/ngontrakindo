# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncDate
from django.db.models import Count, Avg
from django.utils.decorators import method_decorator
from django.http import Http404
from .models import *
from .forms import *
from profiles.models import Profil
from ulasan.models import Rating
from djmoney.models.fields import MoneyPatched
from django.shortcuts import get_object_or_404
from django.core.files.images import get_image_dimensions
from PIL import Image
import string
import random
import arrow
import datetime

def kontrakan_detailview(request, slug):
    obj = ProfilKontrakan.objects.get(slug=slug)
    owner = User.objects.get(id=obj.pemilik.id)
    owner_detail = Profil.objects.get(user=owner)
    fas = Fasilitas.objects.get(kontrakan=obj)
    ulasan = Rating.objects.filter(kontrakan=obj)   
    t_rating = ulasan.aggregate(Avg('rating'))
    l_fr = ["Kasur","Lemari","TV","AC","WiFi","Dapur"]
    fr = [fas.kasur,fas.lemari,fas.tv,fas.ac,fas.wifi,fas.dapur]
    l_fu = ["Laundry","Jemuran","Parkir Mobil","Parkir Motor","Gerbang","Satpam","CCTV"]
    fu = [fas.laundry,fas.jemuran,fas.parkir_mobil,fas.parkir_motor,fas.gerbang,fas.satpam,fas.cctv]
    l_mck = ["Kamar Mandi Dalam","Kamar Mandi Luar","Kloset Jongkok","Kloset Duduk","Shower","Wastafel"]
    mck = [fas.kamar_mandi_dalam,fas.kamar_mandi_luar,fas.kloset_jongkok,fas.kloset_duduk,fas.shower,fas.wastafel]
    l_ls = ["Pasar","Mall","Rumah Makan","Rumah Sakit","Mini Market","Stasiun","Terminal Bus","Akses Tol"]
    ls = [fas.pasar,fas.mall,fas.rumah_makan,fas.rumah_sakit,fas.mini_market,fas.stasiun,fas.terminal_bus,fas.akses_tol]
    biaya = Administrasi.objects.get(kontrakan=obj)
    sisa = obj.n_unit - obj.n_penghuni
    galeri = FotoKontrakan.objects.filter(kontrakan=obj)
    form = PenghuniForm(request.POST or None)
    penghuni = []
    p_detail = []
    if request.method == 'POST':
        if form.is_valid():
            f = form.save(commit=False)
            u = form.cleaned_data.get("user")
            k = form.cleaned_data.get("kontrakan")
            f.user = u
            f.kontrakan = k
            f.save()
            return HttpResponseRedirect("/k/%s" % obj.slug)
        elif request.POST['form'] == 'ulasan':
            r = Rating()
            r.user = request.user
            r.kontrakan = obj
            r.rating = request.POST['rating']
            r.ulasan = request.POST['ulasan']
            r.balasan = ''
            r.save()
            return HttpResponseRedirect("/k/%s" % obj.slug)

    cek_ulasan = False

    if request.user.is_authenticated():
        pengunjung = Profil.objects.get(user=request.user)
        cek_ulasan = ulasan.filter(user=request.user).exists()

        if (obj.kategori == '3' and pengunjung.jk == 'P') or (obj.kategori == '4' and pengunjung.jk == 'L'):
            gender = True
        else:
            gender = False
        cek_penghuni = Penghuni.objects.filter(user=request.user,kontrakan=obj)
        phn = Penghuni.objects.filter(kontrakan=obj,aktif=True,konfirm=True)
        if not cek_penghuni.exists():
            p_status = "visitor"
        else:
            cp = cek_penghuni.last()
            if not cp.aktif and not cp.konfirm:
                p_status = "pending"

            elif not cp.aktif and cp.konfirm:
                p_status = "eks"

            else:
                p_status = "penghuni"

        for c in phn:
            p = Profil.objects.get(user=c.user)
            d = User.objects.get(id=c.user.id)
            penghuni.append(p)
            p_detail.append(d)
    else:
        pengunjung = 'AnonymousUser'
        cek_penghuni = 'AnonymousUser'
        penghuni = 'AnonymousUser'
        # zipped = 'AnonymousUser'
        p_status = "AnonymousUser"
        gender = False

    
    if sisa == 0:
        x = "penuh"
    elif sisa <= 2:
        x = "alert"
    else:
        x = "tersedia"

    if obj.kategori == '1' or obj.kategori == '2':
        kat = "Kontrakan"
    else:
        kat = "Kost"

    if obj.kategori == '1':
        warna = 'w3-green'
    elif obj.kategori == '2':
        warna = 'w3-indigo'
    elif obj.kategori == '3':
        warna = 'w3-brown'
    elif obj.kategori == '4':
        warna = 'w3-pink'
    elif obj.kategori == '5':
        warna = 'w3-purple'

    if not request.user == obj.pemilik:
        obj.dilihat += 1
        obj.save()
        viewer = KontarkanViewer()
        viewer.user = request.user
        viewer.kontrakan = obj
        viewer.save()

    u_ul = []
    p_ul = []
    for u in ulasan:
        u_ul.append(User.objects.get(id=u.user.id))
        p_ul.append(Profil.objects.get(user=u.user))

    today = datetime.datetime.now()

    print(pengunjung)
    context = {
        "kontrakan": obj,
        "fasil": fas,
        "biaya": biaya,
        "pemilik": owner,
        "detail": owner_detail,
        "sisa": x,
        "n": sisa,
        "warna": warna,
        "galeri": galeri,
        "pengunjung": pengunjung,
        "cek_penghuni": cek_penghuni,
        "p_status": p_status,
        "form": form,
        "t_rating": t_rating,
        "gender": gender,
        "penghuni": penghuni,
        "ulasan": ulasan,
        "cek_ulasan": cek_ulasan,
        "zipped": zip(penghuni, p_detail),
        "today": today,
        "z_ul": zip(u_ul,p_ul,ulasan),
        "z_fr": zip(l_fr,fr),
        "z_fu": zip(l_fu,fu),
        "z_mck": zip(l_mck,mck),
        "z_ls": zip(l_ls,ls),
        "kat": kat
	}

    return render(request, "kontrakan_detail.html", context)

@method_decorator(login_required, name='dispatch')
class KontrakanView(FormView):
    template_name = 'form_kontrakan.html'
    form_class = KontrakanForm

    # @login_required(login_url='/accounts/login/')
    def form_valid(self, form):
        f = form.save(commit=False)
        f.pemilik = self.request.user
        f.save()
        u = Profil.objects.get(user=self.request.user)
        u.user_type = '1'
        u.save()
        return redirect('form_fasilitas')

@method_decorator(login_required, name='dispatch')
class DaftarView(FormView):
    template_name = 'form_daftar.html'
    form_class = DaftarForm

    # @login_required(login_url='/accounts/login/')
    def form_valid(self, form):
        f = form.save(commit=False)
        f.pemilik = self.request.user
        f.save()
        u = Profil.objects.get(user=self.request.user)
        u.user_type = '1'
        u.save()
        return redirect('dashboard')

@method_decorator(login_required, name='dispatch')
class FasilitasView(FormView):
    template_name = 'form_fasilitas.html'
    form_class = FasilitasForm

    # @login_required(login_url='/accounts/login/')
    def form_valid(self, form):
        f = form.save(commit=False)
        k = ProfilKontrakan.objects.filter(pemilik=self.request.user)
        f.kontrakan = k.last()
        f.save()
        return redirect('form_administrasi')

@method_decorator(login_required, name='dispatch')
class AdministrasiView(FormView):
    template_name = 'form_administrasi.html'
    form_class = AdministrasiForm

    # @login_required(login_url='/accounts/login/')
    def form_valid(self, form):
        f = form.save(commit=False)
        k = ProfilKontrakan.objects.filter(pemilik=self.request.user)
        kont = k.last()
        f.kontrakan = kont
        f.save()
        return HttpResponseRedirect("/k/%s" % kont.slug)

@login_required(login_url='/accounts/login/')
def admin_view(request):
    u = Profil.objects.get(user=request.user)
    if u.user_type == '1':
        kontrakan = Daftar.objects.filter(pemilik=request.user).order_by('tanggal_daftar')
    context = {
        "pemilik": u,
        "kontrakan": kontrakan,
    }

    return render(request, "dashboard.html", context)

@login_required(login_url='/accounts/login/')
def dashboard_view(request, slug):
    kontrakan = ProfilKontrakan.objects.get(slug=slug)
    a = ProfilKontrakan.objects.filter(slug=slug,pemilik=request.user)
    b = Pengurus.objects.filter(kontrakan=kontrakan,user=request.user)
    if not a.exists() and not b.exists():
        raise Http404("Data Tidak Ditemukan!")

    u = Profil.objects.get(user=request.user)
    rating = Rating.objects.filter(kontrakan=kontrakan)
    r = rating.aggregate(Avg('rating'))
    ulasan = rating.count()
    today = datetime.datetime.now()
    p_user = Penghuni.objects.filter(kontrakan=kontrakan,aktif=True,konfirm=True).count()
    p_non = kontrakan.n_penghuni - p_user
    kosong = kontrakan.n_unit-(p_user+p_non)
    z_pie = [p_user,p_non,kosong]
    viw = KontarkanViewer.objects.filter(kontrakan=kontrakan).datetimes('timestamp', 'day').annotate(Count('id'))
    viewer = KontarkanViewer.objects.filter(kontrakan=kontrakan).annotate(day=TruncDate('timestamp')).values('day').annotate(viewer=Count('id')).values('viewer','day').order_by('day')
    
    tgl = []
    vi = []
    for v in viw:
        tgl.append(v.date())
    for c in viewer:
        vi.append(c['viewer'])

    if kontrakan.kategori == '1' or kontrakan.kategori == '2':
        kat = "Kontrakan"
    else:
        kat = "Kost"

    if u.user_type == '2':
        png = Pengurus.objects.get(user=request.user)
    else:
        png = ''

    context = {
        "pemilik": u,
        "kontrakan": kontrakan,
        "kat": kat,
        "png": png,
        "viw": viw,
        "tgl": tgl,
        "rating": r,
        "ulasan": ulasan,
        "today": today,
        "vi": vi,
        "z_pie": z_pie,
        "title": "Dashboard",
    }

    return render(request, "dashboard2.html", context)

@login_required(login_url='/accounts/login/')
def kontrakan_view(request, slug):
    u = Profil.objects.get(user=request.user)
    kontrakan = ProfilKontrakan.objects.get(slug=slug)
    fasilitas = Fasilitas.objects.get(kontrakan=kontrakan)
    biaya = Administrasi.objects.get(kontrakan=kontrakan)
    if kontrakan.kategori == '1' or kontrakan.kategori == '2':
        kat = "Kontrakan"
    else:
        kat = "Kost"

    form = FasilitasForm(request.POST or None,
        initial={
            'luas': fasilitas.luas,
            'listrik': fasilitas.listrik,
            'air': fasilitas.air,
            'kasur': fasilitas.kasur,
            'lemari': fasilitas.lemari,
            'tv': fasilitas.tv,
            'ac': fasilitas.ac,
            'wifi': fasilitas.wifi,
            'kamar_mandi_dalam': fasilitas.kamar_mandi_dalam,
            'kamar_mandi_luar': fasilitas.kamar_mandi_luar,
            'kloset_duduk': fasilitas.kloset_duduk,
            'kloset_jongkok': fasilitas.kloset_jongkok,
            'shower': fasilitas.shower,
            'wastafel': fasilitas.wastafel,
            'dapur': fasilitas.dapur,
            'laundry': fasilitas.laundry,
            'jemuran': fasilitas.jemuran,
            'parkir_mobil': fasilitas.parkir_mobil,
            'parkir_motor': fasilitas.parkir_motor,
            'gerbang': fasilitas.gerbang,
            'satpam': fasilitas.satpam,
            'cctv': fasilitas.cctv,
            'rumah_sakit': fasilitas.rumah_sakit,
            'rumah_makan': fasilitas.rumah_makan,
            'pasar': fasilitas.pasar,
            'mall': fasilitas.mall,
            'mini_market': fasilitas.mini_market,
            'stasiun': fasilitas.stasiun,
            'terminal_bus': fasilitas.terminal_bus,
            'akses_tol': fasilitas.akses_tol,
            'fasilitas_lain': fasilitas.fasilitas_lain,
        })

    form2 = AdministrasiForm(request.POST or None,
        initial={
            'penghuni_max': biaya.penghuni_max,
            'harian': biaya.harian,
            'per_hari': biaya.per_hari,
            'mingguan': biaya.mingguan,
            'per_minggu': biaya.per_minggu,
            'bulanan': biaya.bulanan,
            'per_bulan': biaya.per_bulan,
            'tahunan': biaya.tahunan,
            'per_tahun': biaya.per_tahun,
            'denda': biaya.denda,
            'syarat_ketentuan': biaya.syarat_ketentuan,
        })

    form3 = KontrakanEditForm(request.POST or None,
        initial={
            # 'lokasi': kontrakan.lokasi,
            'alamat': kontrakan.alamat,
            'kategori': kontrakan.kategori,
            'nama': kontrakan.nama,
            'n_unit': kontrakan.n_unit,
            'n_penghuni': kontrakan.n_penghuni,
            'status': kontrakan.status,
            'deskripsi': kontrakan.deskripsi,
    })

    if request.method == 'POST':
        print(form3.has_changed())
        print(form.has_changed())
        print(form2.has_changed())

    if u.user_type == '2':
        png = Pengurus.objects.get(user=request.user)
    else:
        png = ''

    context = {
        "pemilik": u,
        "kontrakan": kontrakan,
        "kat": kat,
        "png": png,
        "form": form,
        "form2": form2,
        "form3": form3,
        "title": "Kontrakan",
    }

    return render(request, "kontrakanview.html", context)

@login_required(login_url='/accounts/login/')
def galeri_view(request, slug):
    u = Profil.objects.get(user=request.user)
    kontrakan = ProfilKontrakan.objects.get(slug=slug)
    if kontrakan.kategori == '1' or kontrakan.kategori == '2':
        kat = "Kontrakan"
    else:
        kat = "Kost"

    form = GaleriForm(request.POST, request.FILES)

    if request.method == 'POST':
        if form.is_valid():
            img = form.save(commit=False)
            x = form.cleaned_data.get('x')
            y = form.cleaned_data.get('y')
            w = form.cleaned_data.get('width')
            h = form.cleaned_data.get('height')
            img.kontrakan = kontrakan
            img.save()
            f = FotoKontrakan.objects.filter(kontrakan=kontrakan)
            if f.count() == 1:
                f.update(foto_utama=True)
            return HttpResponseRedirect("/administrasi/galeri/%s" % kontrakan.slug)
        elif request.POST['pencet'] == 'utama':
            FotoKontrakan.objects.filter(kontrakan=kontrakan).update(foto_utama=False)
            gambar = FotoKontrakan.objects.get(id=request.POST['gambar'])
            gambar.foto_utama = True
            gambar.save()
            return HttpResponseRedirect("/administrasi/galeri/%s" % kontrakan.slug)
        elif request.POST['pencet'] == 'hapus':
            gambar = FotoKontrakan.objects.get(id=request.POST['gambar'])
            gambar.delete()
            return HttpResponseRedirect("/administrasi/galeri/%s" % kontrakan.slug)

    else:
        form = GaleriForm()
    
    galeri = FotoKontrakan.objects.filter(kontrakan=kontrakan).order_by('tanggal_upload')

    if u.user_type == '2':
        png = Pengurus.objects.get(user=request.user)
    else:
        png = ''

    context = {
        "pemilik": u,
        "kontrakan": kontrakan,
        "kat": kat,
        "png": png,
        "galeri": galeri,
        "title": "Galeri",
        "form": form,
    }

    return render(request, "galeri.html", context)

@login_required(login_url='/accounts/login/')
def penghuni_view(request, slug):
    u = Profil.objects.get(user=request.user)
    kontrakan = ProfilKontrakan.objects.get(slug=slug)
    penghuni = Penghuni.objects.filter(kontrakan=kontrakan,aktif=True,konfirm=True)
    p_detail = []
    u_detail = []
    for ph in penghuni:
        p_detail.append(Profil.objects.get(user=ph.user))
        u_detail.append(User.objects.get(id=ph.user.id))

    z_detail = zip(p_detail, u_detail, penghuni)
    baru = Penghuni.objects.filter(kontrakan=kontrakan,aktif=False,konfirm=False)
    p_baru = []
    u_baru = []
    for b in baru:
        p_baru.append(Profil.objects.get(user=b.user))
        u_baru.append(User.objects.get(id=b.user.id))

    z_baru = zip(p_baru, u_baru)
    eks = Penghuni.objects.filter(kontrakan=kontrakan,aktif=False,konfirm=True)
    p_eks = []
    u_eks = []
    for e in eks:
        p_eks.append(Profil.objects.get(user=e.user))
        u_eks.append(User.objects.get(id=e.user.id))

    z_eks = zip(p_eks, u_eks, eks)
    if kontrakan.kategori == '1' or kontrakan.kategori == '2':
        kat = "Kontrakan"
    else:
        kat = "Kost"

    if request.method == 'POST':
        konf = request.POST['konfirm']
        us = request.POST['user']
        x = User.objects.get(username=us)
        if konf == 'yes':
            termasuk = request.POST['termasuk']
            if termasuk == 'n':
                kontrakan.n_penghuni += 1
                kontrakan.save()

            cari = Penghuni.objects.get(user=x,kontrakan=kontrakan,aktif=False,konfirm=False)
            cari.aktif = True
            cari.konfirm = True
            cari.tanggal_masuk = datetime.datetime.now()
            cari.save()
            return HttpResponseRedirect("/administrasi/penghuni/%s" % kontrakan.slug)
        else:
            cari = Penghuni.objects.get(user=x,kontrakan=kontrakan,aktif=False,konfirm=False)
            cari.delete()
            return HttpResponseRedirect("/administrasi/penghuni/%s" % kontrakan.slug)
    
    if u.user_type == '2':
        png = Pengurus.objects.get(user=request.user)
    else:
        png = ''

    context = {
        "pemilik": u,
        "kontrakan": kontrakan,
        "kat": kat,
        "png": png,
        "title": "Penghuni",
        "penghuni": penghuni,
        "baru": baru,
        "eks": eks,
        "z_baru": z_baru,
        "z_eks": z_eks,
        "z_detail": z_detail,
    }

    return render(request, "penghuni.html", context)

@login_required(login_url='/accounts/login/')
def ulasan_view(request, slug):
    us = Profil.objects.get(user=request.user)
    kontrakan = ProfilKontrakan.objects.get(slug=slug)
    ulasan = Rating.objects.filter(kontrakan=kontrakan)
    r = ulasan.aggregate(Avg('rating'))
    p_ul = []
    u_ul = []
    for u in ulasan:
        p_ul.append(Profil.objects.get(user=u.user))
        u_ul.append(User.objects.get(id=u.user.id))

    if request.method == 'POST':
        ul = Rating.objects.get(id=request.POST['id'])
        ul.balasan = request.POST['balas']
        ul.tgl_balas = datetime.datetime.now()
        ul.save()
        return HttpResponseRedirect("/administrasi/ulasan/%s" % kontrakan.slug)

    if kontrakan.kategori == '1' or kontrakan.kategori == '2':
        kat = "Kontrakan"
    else:
        kat = "Kost"

    if us.user_type == '2':
        png = Pengurus.objects.get(user=request.user)
    else:
        png = ''

    context = {
        "pemilik": us,
        "kontrakan": kontrakan,
        "rating": r,
        "png": png,
        "kat": kat,
        "ulasan": ulasan,
        "z_ul": zip(p_ul, u_ul, ulasan),
        "title": "Ulasan",
    }

    return render(request, "ulasan.html", context)


@login_required(login_url='/accounts/login/')
def user_view(request, slug):
    u = Profil.objects.get(user=request.user)
    kontrakan = ProfilKontrakan.objects.get(slug=slug)
    own = Profil.objects.get(user=kontrakan.pemilik)
    u_own = User.objects.get(id=kontrakan.pemilik.id)

    if kontrakan.kategori == '1' or kontrakan.kategori == '2':
        kat = "Kontrakan"
    else:
        kat = "Kost"

    if request.method == 'POST':
        us = User()
        us.first_name = request.POST['nama_depan']
        us.last_name = request.POST['nama_belakang']
        us.username = request.POST['username']
        us.email = request.POST['email']
        password = request.POST['pwd1']
        us.set_password(password)
        us.save()

        pr = Profil()
        pr.user = User.objects.get(username=request.POST['username'])
        pr.user_type = '2'
        pr.save()

        png = Pengurus()
        png.user = User.objects.get(username=request.POST['username'])
        png.kontrakan = kontrakan
        if "edit_kontrakan" in request.POST:
            png.edit_kontrakan = True
        if "konfirm_penghuni" in request.POST:
            png.konfirm_penghuni = True
        if "transaksi" in request.POST:
            png.transaksi = True
        if "galeri" in request.POST:
            png.galeri = True
        if "ulasan" in request.POST:
            png.ulasan = True
        png.save()

        return HttpResponseRedirect("/administrasi/user/%s" % kontrakan.slug)

    pengurus = Pengurus.objects.filter(kontrakan=kontrakan)
    p_peng = []
    u_peng = []
    if pengurus.exists():
        for p in pengurus:
            p_peng.append(Profil.objects.get(user=p.user))
            u_peng.append(User.objects.get(id=p.user.id))

    if u.user_type == '2':
        png = Pengurus.objects.get(user=request.user)
    else:
        png = ''

    context = {
        "kat": kat,
        "own": own,
        "u_own": u_own,
        "pemilik": u,
        "png": png,
        "pengurus": pengurus,
        "z_peng": zip(pengurus, p_peng, u_peng),
        "kontrakan": kontrakan,
        "title": "User",
    }

    return render(request, "user.html", context)


@login_required(login_url='/accounts/login/')
def transaksi_view(request, slug):
    u = Profil.objects.get(user=request.user)
    kontrakan = ProfilKontrakan.objects.get(slug=slug)
    penghuni = Penghuni.objects.filter(kontrakan=kontrakan,aktif=True,konfirm=True)
    p_detail = []
    u_detail = []
    transaksi = []
    for ph in penghuni:
        p_detail.append(Profil.objects.get(user=ph.user))
        u_detail.append(User.objects.get(id=ph.user.id))
        transaksi.append(Transaksi.objects.filter(penghuni=ph))

    z_detail = zip(p_detail, u_detail, penghuni, transaksi)
    if kontrakan.kategori == '1' or kontrakan.kategori == '2':
        kat = "Kontrakan"
    else:
        kat = "Kost"

    context = {
        "kat": kat,
        "pemilik": u,
        "penghuni": penghuni,
        "z_detail": z_detail,
        "kontrakan": kontrakan,
        "title": "Transaksi",
    }

    return render(request, "transaksi.html", context)