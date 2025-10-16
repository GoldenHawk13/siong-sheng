import streamlit as st

# Set page configuration
st.set_page_config(page_title="Siong Sheng Supermarket", page_icon="🛒", layout="wide")

# Product catalog with prices
PRODUCTS = {
    "Fresh Produce": {
        "Bananas (1kg)": 2.50,
        "Apples (1kg)": 4.80,
        "Tomatoes (500g)": 3.20,
        "Carrots (500g)": 2.00,
        "Onions (1kg)": 3.50
    },
    "Meat & Seafood": {
        "Chicken Breast (500g)": 8.90,
        "Pork Belly (500g)": 12.50,
        "Salmon Fillet (200g)": 15.80,
        "Prawns (250g)": 18.90,
        "Minced Beef (500g)": 11.20
    },
    "Dairy & Eggs": {
        "Fresh Milk (1L)": 3.80,
        "Greek Yogurt (500g)": 5.50,
        "Cheese Slices (200g)": 4.20,
        "Eggs (12 pieces)": 6.80,
        "Butter (250g)": 7.50
    },
    "Pantry Essentials": {
        "Jasmine Rice (5kg)": 18.90,
        "Cooking Oil (1L)": 8.50,
        "Soy Sauce (500ml)": 3.80,
        "Bread (1 loaf)": 2.80,
        "Pasta (500g)": 3.20
    },
    "Beverages": {
        "Mineral Water (1.5L)": 1.20,
        "Orange Juice (1L)": 4.50,
        "Green Tea (500ml)": 2.80,
        "Coffee (200g)": 12.80,
        "Soft Drink (1.5L)": 3.50
    }
}

# Loyalty tier system
def get_loyalty_discount(points):
    """Calculate discount based on loyalty points"""
    if points >= 8000:
        return 0.12, "💎 Platinum"
    elif points >= 3000:
        return 0.08, "🥇 Gold"
    elif points >= 1000:
        return 0.05, "🥈 Silver"
    else:
        return 0.02, "🥉 Bronze"

def get_points_multiplier(points):
    """Get points earning multiplier based on tier"""
    if points >= 8000:
        return 2.0
    elif points >= 3000:
        return 1.5
    elif points >= 1000:
        return 1.2
    else:
        return 1.0

def calculate_bulk_discount(total_items):
    """Calculate bulk purchase discount"""
    if total_items >= 20:
        return 0.10
    elif total_items >= 15:
        return 0.07
    elif total_items >= 10:
        return 0.05
    else:
        return 0.0

def calculate_points_earned(amount, multiplier):
    """Calculate points earned (2 points per dollar with multiplier)"""
    base_points = int(amount * 2)
    return int(base_points * multiplier)

def main():
    st.title("🛒 Siong Sheng Supermarket")
    st.subheader("Your Neighborhood Fresh Market")
    
    # Sidebar - Customer info
    st.sidebar.header("👤 Customer Information")
    customer_points = st.sidebar.number_input(
        "Enter customer loyalty points:",
        min_value=0,
        max_value=50000,
        value=1500,
        step=100
    )
    
    # Get customer tier info
    tier_discount, tier_name = get_loyalty_discount(customer_points)
    points_multiplier = get_points_multiplier(customer_points)
    
    # Display tier info in sidebar
    st.sidebar.write(f"**Current Tier:** {tier_name}")
    st.sidebar.write(f"**Tier Discount:** {tier_discount*100:.0f}%")
    st.sidebar.write(f"**Points Multiplier:** {points_multiplier:.1f}x")
    
    # Calculate next tier progress
    if customer_points < 1000:
        next_tier = "Silver"
        points_needed = 1000 - customer_points
    elif customer_points < 3000:
        next_tier = "Gold"
        points_needed = 3000 - customer_points
    elif customer_points < 8000:
        next_tier = "Platinum"
        points_needed = 8000 - customer_points
    else:
        next_tier = None
        points_needed = 0
    
    if next_tier:
        st.sidebar.write(f"**Next Tier:** {next_tier}")
        st.sidebar.write(f"**Points Needed:** {points_needed:,}")
    else:
        st.sidebar.write("**Status:** Maximum tier achieved! 💎")
    
    # Main content area
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.header("🛍️ Product Selection")
        
        # Initialize variables
        shopping_cart = []
        total_items = 0
        subtotal = 0.0
        
        # Display products by category
        for category, products in PRODUCTS.items():
            st.subheader(f"{category}")
            
            # Create two columns for products
            product_col1, product_col2 = st.columns(2)
            
            product_list = list(products.items())
            
            # Display products in two columns
            for i in range(0, len(product_list), 2):
                # First column
                with product_col1:
                    if i < len(product_list):
                        item_name, price = product_list[i]
                        quantity = st.number_input(
                            f"{item_name}\n${price:.2f}",
                            min_value=0,
                            max_value=50,
                            value=0,
                            step=1,
                            key=f"{category}_{item_name}_1"
                        )
                        
                        if quantity > 0:
                            item_total = quantity * price
                            shopping_cart.append({
                                "category": category,
                                "name": item_name,
                                "price": price,
                                "quantity": quantity,
                                "total": item_total
                            })
                            total_items += quantity
                            subtotal += item_total
                
                # Second column
                with product_col2:
                    if i + 1 < len(product_list):
                        item_name, price = product_list[i + 1]
                        quantity = st.number_input(
                            f"{item_name}\n${price:.2f}",
                            min_value=0,
                            max_value=50,
                            value=0,
                            step=1,
                            key=f"{category}_{item_name}_2"
                        )
                        
                        if quantity > 0:
                            item_total = quantity * price
                            shopping_cart.append({
                                "category": category,
                                "name": item_name,
                                "price": price,
                                "quantity": quantity,
                                "total": item_total
                            })
                            total_items += quantity
                            subtotal += item_total
    
    with col2:
        st.header("🧾 Order Summary")
        
        if shopping_cart:
            # Display shopping cart
            st.write("**Shopping Cart:**")
            
            # Group items by category for display
            current_category = ""
            for item in shopping_cart:
                if item["category"] != current_category:
                    current_category = item["category"]
                    st.write(f"*{current_category}:*")
                
                st.write(f"• {item['name']}")
                st.write(f"  Qty: {item['quantity']} | ${item['total']:.2f}")
            
            st.write("---")
            
            # Calculate discounts
            tier_discount_amount = subtotal * tier_discount
            bulk_discount_rate = calculate_bulk_discount(total_items)
            bulk_discount_amount = subtotal * bulk_discount_rate
            
            # Apply discounts
            total_discount = tier_discount_amount + bulk_discount_amount
            discounted_subtotal = subtotal - total_discount
            
            # Calculate GST
            gst_amount = discounted_subtotal * 0.08
            final_total = discounted_subtotal + gst_amount
            
            # Calculate points earned
            points_earned = calculate_points_earned(subtotal, points_multiplier)
            
            # Display price breakdown
            st.write("**Price Breakdown:**")
            st.write(f"Items Subtotal: ${subtotal:.2f}")
            
            if tier_discount_amount > 0:
                st.write(f"{tier_name} Discount ({tier_discount*100:.0f}%): -${tier_discount_amount:.2f}")
            
            if bulk_discount_amount > 0:
                st.write(f"Bulk Discount ({bulk_discount_rate*100:.0f}%): -${bulk_discount_amount:.2f}")
            
            st.write(f"GST (8%): ${gst_amount:.2f}")
            st.write("---")
            st.write(f"**FINAL TOTAL: ${final_total:.2f}**")
            
            # Points section
            st.write("**Loyalty Points:**")
            st.write(f"Points earned: {points_earned:,}")
            st.write(f"Total after purchase: {customer_points + points_earned:,}")
            
            # Show savings
            if total_discount > 0:
                st.success(f"💰 You saved ${total_discount:.2f}!")
            
            # Show tier upgrade notification
            new_total_points = customer_points + points_earned
            if next_tier and new_total_points >= (1000 if next_tier == "Silver" else 3000 if next_tier == "Gold" else 8000):
                st.balloons()
                st.success(f"🎉 Congratulations! You've reached {next_tier} tier!")
            
            # Receipt button
            if st.button("🖨️ Generate Receipt", type="primary"):
                st.write("**RECEIPT**")
                st.write("="*50)
                st.write("SIONG SHENG SUPERMARKET")
                st.write("Your Neighborhood Fresh Market")
                st.write("="*50)
                st.write(f"Customer Tier: {tier_name}")
                st.write(f"Existing Points: {customer_points:,}")
                st.write("-"*50)
                
                # Items
                current_cat = ""
                for item in shopping_cart:
                    if item["category"] != current_cat:
                        current_cat = item["category"]
                        st.write(f"\n{current_cat.upper()}:")
                    st.write(f"{item['name']} x{item['quantity']} = ${item['total']:.2f}")
                
                st.write("-"*50)
                st.write(f"Subtotal: ${subtotal:.2f}")
                if tier_discount_amount > 0:
                    st.write(f"{tier_name} Discount: -${tier_discount_amount:.2f}")
                if bulk_discount_amount > 0:
                    st.write(f"Bulk Discount: -${bulk_discount_amount:.2f}")
                st.write(f"GST (8%): ${gst_amount:.2f}")
                st.write("="*50)
                st.write(f"TOTAL: ${final_total:.2f}")
                st.write(f"Points Earned: +{points_earned:,}")
                st.write(f"New Points Balance: {new_total_points:,}")
                st.write("="*50)
                st.write("Thank you for shopping with us!")
        
        else:
            st.info("Add items to your cart to see the total!")
            
            # Show tier benefits
            st.write("**Loyalty Tier Benefits:**")
            st.write("🥉 **Bronze** (0-999 pts): 2% discount, 1.0x points")
            st.write("🥈 **Silver** (1,000-2,999 pts): 5% discount, 1.2x points")
            st.write("🥇 **Gold** (3,000-7,999 pts): 8% discount, 1.5x points")
            st.write("💎 **Platinum** (8,000+ pts): 12% discount, 2.0x points")
            
            st.write("\n**Bulk Purchase Discounts:**")
            st.write("• 10-14 items: 5% off")
            st.write("• 15-19 items: 7% off")
            st.write("• 20+ items: 10% off")
            
            st.write("\n**Points System:**")
            st.write("• Earn 2 points per $1 spent")
            st.write("• Higher tiers earn bonus points")
    
    # Footer
    st.write("---")
    st.write("*Siong Sheng Supermarket - Fresh. Quality. Value! 🥬🥩🥛*")

if __name__ == "__main__":
    main()

