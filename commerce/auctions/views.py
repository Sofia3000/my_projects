from xml.dom.minidom import Attr
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from decimal import *

from .models import User, Category, Comment, Auction, Rate
from . import utils

class NewAuctionForm(forms.Form):
    name = forms.CharField(max_length=60, label='', widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Name'}))
    review = forms.CharField(max_length=200, label='', widget=forms.Textarea(attrs={'class' : 'form-control', 'placeholder': 'Short review'}))
    start_rate = forms.DecimalField(max_digits=20, label='', decimal_places=2, min_value=0.0, widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder': 'Start rate'}))
    category = forms.ChoiceField(label='Category (optional)', choices = utils.get_categories(), required=False)
    image = forms.ImageField(label='Image (optional)', required=False)

def index(request):
    auctions = Auction.objects.filter(isactive=True)
    infolist = []
    for auction in auctions:
        max_rate = auction.rates.order_by('-price').first()
        current_price = max_rate.price if max_rate else auction.start_rate
        d = {}
        d["auction"]=auction
        d["current_price"]=current_price
        infolist.append(d)
    return render(request, "auctions/index.html",{
        "infolist": infolist
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        
        # Check data
        if not username or not password:
            return render(request, "auctions/login.html", {
                "message": "You must enter all fields."
            })
            
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    # log out
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        # Check data
        if not username or not email or not password or not confirmation:
            return render(request, "auctions/register.html", {
                "message": "You must enter all fields."
            })
        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_auction(request):
    if request.method == "POST":
        # Get data from request
        form = NewAuctionForm(request.POST, request.FILES)
        # Validate form
        if form.is_valid():
            try:
                cur_category = Category.objects.get(id=form.cleaned_data['category'])
            except ValueError:
                cur_category = None
            except Category.DoesNotExist:
                cur_category = None
            # Create new auction
            auction = Auction(name = form.cleaned_data['name'], review = form.cleaned_data['review'], 
            start_rate = form.cleaned_data['start_rate'], category = cur_category,
            image = form.cleaned_data['image'], owner = request.user)
            auction.save()
            return HttpResponseRedirect(reverse('index'))
        # Show error message
        return  render(request, "auctions/newauction.html", {
            "form": form,
            "message": "You input uncorrect data."
        })
    return  render(request, "auctions/newauction.html", {
        "form": NewAuctionForm()
    })


def watch_auction(request, id):
    # Get auction with specified id
    try:
        auction = Auction.objects.get(id=id)
        max_rate = auction.rates.order_by('-price').first()
    except ValueError:
        return HttpResponseRedirect(reverse("index"))
    except Auction.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))
    # Get all comments about auction
    comments = auction.comments.all()
    # Show information
    return render(request, "auctions/auction.html", {
        "auction": auction,
        "max_rate": max_rate,
        "comments":comments
    })

@login_required
def change_watchlist(request):
    if request.method == "POST":
        auction_id = request.POST.get("id", None)
        action = request.POST.get("action", None)
        # Validate data
        if auction_id and action:
            # Get auction
            try:
                auction = Auction.objects.get(id=auction_id, isactive=True)
            except ValueError:
                return HttpResponseRedirect(reverse("index"))
            except Auction.DoesNotExist:
                return HttpResponseRedirect(reverse("index"))
            # Check if user is not owner
            if auction.owner != request.user:
                # Add auction to watchlist
                if action == "add":
                    if not auction in request.user.watchlist.all():
                        request.user.watchlist.add(auction)
                # Delete auction from watchlist
                elif action == "delete":
                    if auction in request.user.watchlist.all():
                        request.user.watchlist.remove(auction)
            return HttpResponseRedirect(reverse("auction", args=(auction_id,)))
    return HttpResponseRedirect(reverse("index"))

@login_required
def new_rate(request):
    if request.method == "POST":
        auction_id = request.POST.get("id", None)
        price_txt = request.POST.get("price", None)
        # Validate data
        if auction_id and price_txt:
            # Get auction
            try:
                auction = Auction.objects.get(id=auction_id, isactive=True)
            except ValueError:
                return HttpResponseRedirect(reverse("index"))
            except Auction.DoesNotExist:
                return HttpResponseRedirect(reverse("index"))
            # Check if user is not owner
            if auction.owner != request.user:
                # Convert price to Decimal
                try:
                    price = Decimal(price_txt)
                except ValueError:
                    return render(request, "auctions/newrate.html", {
                        "auction_id": auction_id,
                        "class_name": "alert-danger",
                        "message": "Error! Rate must be a number."
                    })
                # Compare rate with max rate
                max_rate = auction.rates.order_by('-price').first()
                flag = True
                class_name = ""
                message = ""
                if max_rate:
                    if Decimal(max_rate.price).compare(price) != -1:
                        flag = False
                # Validate price value
                if price >= auction.start_rate and flag:
                    # Save rate
                    rate = Rate(auction=auction, user=request.user, price=price)
                    rate.save()
                    class_name = "alert-success"
                    message = f"You made a rate successfully!"
                else:
                    class_name = "alert-danger"
                    message = "Error! Your rate must be greater than or equal start rate and greater than current price."
                # Show message with result 
                return render(request, "auctions/newrate.html", {
                    "auction_id": auction_id,
                    "class_name": class_name,
                    "message": message
                })       
            return HttpResponseRedirect(reverse("auction", args=(auction_id,)))
    return HttpResponseRedirect(reverse("index"))

@login_required
def close_auction(request):
    if request.method == "POST":
        auction_id = request.POST.get("id", None)
        if auction_id:
            # Get auction
            try:
                auction = Auction.objects.get(id=auction_id, isactive=True)
            except ValueError:
                return HttpResponseRedirect(reverse("index"))
            except Auction.DoesNotExist:
                return HttpResponseRedirect(reverse("index"))
            # Check if user is owner
            if auction.owner == request.user:
                # Close auction
                auction.isactive = False
                auction.save()
            return HttpResponseRedirect(reverse("auction", args=(auction_id,)))
    return HttpResponseRedirect(reverse("index"))

@login_required
def new_comment(request):
    if request.method == "POST":
        auction_id = request.POST.get("id", None)
        text = request.POST.get("text", None)
        # Validate data
        if auction_id and text and text.strip():
            # Get auction
            try:
                auction = Auction.objects.get(id=auction_id, isactive=True)
            except ValueError:
                return HttpResponseRedirect(reverse("index"))
            except Auction.DoesNotExist:
                return HttpResponseRedirect(reverse("index"))
            # Check if user is not owner
            if auction.owner != request.user:
                # Save comment
                comment = Comment(auction=auction, user=request.user, text=text)
                comment.save()
            return HttpResponseRedirect(reverse("auction", args=(auction_id,)))
    return HttpResponseRedirect(reverse("index"))

@login_required
def view_watchlist(request):
    # Show auctions from watchlist
    auctions = request.user.watchlist.all()
    return render(request, "auctions/auction_list.html",{
        "header": "Watchlist",
        "auctions": auctions,
        "message":"There are not any auctions in watchlist."
    })

def category_list(request):
    # Show page with categories
    categories = Category.objects.all()
    return render(request, "auctions/category_list.html", {
        "categories":categories
    })

def category(request, id):
    # Get auctions with selected category
    auctions = None
    category = None
    if id == 0:
        auctions = Auction.objects.filter(category=None, isactive=True)
    else:
        try:
            category = Category.objects.get(id=id)
        except ValueError:
            HttpResponseRedirect(reverse('category_list'))
        except Category.DoesNotExist:
            HttpResponseRedirect(reverse('category_list'))
        auctions = category.auctions.filter(isactive=True)
    name = category.name if category else "Without category"
    # Show page with auctions
    return render(request, "auctions/auction_list.html",{
        "header": f'All auctions in category "{name}"',
        "auctions": auctions,
        "message":'There are not any active auctions in this category.'
    })