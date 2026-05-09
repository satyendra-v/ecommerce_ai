from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import ListFlowable, ListItem
from datetime import datetime

OUTPUT_PATH = "./ecommerce_company_knowledge_base.pdf"

doc = SimpleDocTemplate(
    OUTPUT_PATH,
    pagesize=A4,
    rightMargin=2*cm,
    leftMargin=2*cm,
    topMargin=2.5*cm,
    bottomMargin=2.5*cm,
    title="ShopEase eCommerce – Company Knowledge Base",
    author="ShopEase Inc.",
    subject="Company Policies, Logistics, Refund Policy and FAQs",
)

styles = getSampleStyleSheet()

# Custom styles
BRAND_COLOR = colors.HexColor("#1A56DB")
ACCENT_COLOR = colors.HexColor("#E1EFFF")
DARK_COLOR = colors.HexColor("#1E293B")
MUTED_COLOR = colors.HexColor("#64748B")
DIVIDER_COLOR = colors.HexColor("#CBD5E1")

title_style = ParagraphStyle(
    "DocTitle", parent=styles["Title"],
    fontSize=28, textColor=BRAND_COLOR,
    spaceAfter=6, leading=34,
    alignment=TA_CENTER,
)
subtitle_style = ParagraphStyle(
    "DocSubtitle", parent=styles["Normal"],
    fontSize=12, textColor=MUTED_COLOR,
    spaceAfter=4, alignment=TA_CENTER,
)
h1_style = ParagraphStyle(
    "H1", parent=styles["Heading1"],
    fontSize=17, textColor=BRAND_COLOR,
    spaceBefore=18, spaceAfter=6,
    borderPad=4,
)
h2_style = ParagraphStyle(
    "H2", parent=styles["Heading2"],
    fontSize=13, textColor=DARK_COLOR,
    spaceBefore=12, spaceAfter=4,
)
h3_style = ParagraphStyle(
    "H3", parent=styles["Heading3"],
    fontSize=11, textColor=DARK_COLOR,
    spaceBefore=8, spaceAfter=3,
)
body_style = ParagraphStyle(
    "Body", parent=styles["Normal"],
    fontSize=10, textColor=DARK_COLOR,
    leading=15, spaceAfter=6,
    alignment=TA_JUSTIFY,
)
bullet_style = ParagraphStyle(
    "Bullet", parent=body_style,
    leftIndent=14, bulletIndent=0,
    spaceAfter=3,
)
note_style = ParagraphStyle(
    "Note", parent=body_style,
    fontSize=9, textColor=MUTED_COLOR,
    leftIndent=10, italic=True,
)
label_style = ParagraphStyle(
    "Label", parent=body_style,
    fontSize=9, textColor=BRAND_COLOR,
    fontName="Helvetica-Bold", spaceAfter=2,
)

def divider():
    return HRFlowable(width="100%", thickness=1, color=DIVIDER_COLOR, spaceAfter=6, spaceBefore=4)

def bullet(text):
    return Paragraph(f"&#x2022;&nbsp;&nbsp;{text}", bullet_style)

def section_header(text):
    return [Paragraph(text, h1_style), divider()]

story = []

# ─── Cover ───────────────────────────────────────────────────────────────────
story.append(Spacer(1, 2*cm))
story.append(Paragraph("ShopEase", title_style))
story.append(Paragraph("eCommerce Company – Official Knowledge Base", subtitle_style))
story.append(Paragraph("Policies · Logistics · Support · FAQs", subtitle_style))
story.append(Spacer(1, 0.4*cm))

meta_data = [
    ["Document Type", "Company Knowledge Base (RAG-Ready)"],
    ["Company Name", "ShopEase Inc."],
    ["Website", "www.shopease.com"],
    ["Version", "v1.0"],
    ["Effective Date", "01 January 2025"],
    ["Last Updated", datetime.today().strftime("%d %B %Y")],
]
meta_table = Table(meta_data, colWidths=[4.5*cm, 11*cm])
meta_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, -1), ACCENT_COLOR),
    ("TEXTCOLOR", (0, 0), (0, -1), BRAND_COLOR),
    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9.5),
    ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ("BOX", (0, 0), (-1, -1), 0.8, DIVIDER_COLOR),
    ("INNERGRID", (0, 0), (-1, -1), 0.5, DIVIDER_COLOR),
    ("PADDING", (0, 0), (-1, -1), 6),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(meta_table)
story.append(PageBreak())

# ─── Table of Contents ───────────────────────────────────────────────────────
story += section_header("Table of Contents")
toc = [
    ("1.", "About ShopEase", "3"),
    ("2.", "Products & Categories", "3"),
    ("3.", "Ordering Process", "4"),
    ("4.", "Payment Policy", "4"),
    ("5.", "Shipping & Logistics", "5"),
    ("6.", "Refund & Return Policy", "6"),
    ("7.", "Exchange Policy", "7"),
    ("8.", "Cancellation Policy", "8"),
    ("9.", "Customer Support", "8"),
    ("10.", "Privacy Policy", "9"),
    ("11.", "Terms & Conditions", "10"),
    ("12.", "Seller / Vendor Policy", "11"),
    ("13.", "Loyalty Program – ShopEase Rewards", "11"),
    ("14.", "Frequently Asked Questions (FAQs)", "12"),
]
toc_data = [[Paragraph(n, body_style), Paragraph(t, body_style), Paragraph(p, body_style)] for n, t, p in toc]
toc_table = Table(toc_data, colWidths=[1.2*cm, 13.3*cm, 1*cm])
toc_table.setStyle(TableStyle([
    ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ("PADDING", (0, 0), (-1, -1), 5),
    ("ALIGN", (2, 0), (2, -1), "RIGHT"),
    ("INNERGRID", (0, 0), (-1, -1), 0.3, DIVIDER_COLOR),
    ("BOX", (0, 0), (-1, -1), 0.5, DIVIDER_COLOR),
]))
story.append(toc_table)
story.append(PageBreak())

# ─── 1. About ShopEase ───────────────────────────────────────────────────────
story += section_header("1. About ShopEase")
story.append(Paragraph("Company Overview", h2_style))
story.append(Paragraph(
    "ShopEase Inc. is a Singapore-based e-commerce platform founded in 2018, dedicated to delivering "
    "a seamless, fast, and trustworthy online shopping experience across Southeast Asia. We connect "
    "millions of buyers with thousands of verified sellers, offering a diverse catalogue of products "
    "ranging from electronics and fashion to home essentials and groceries.",
    body_style))
story.append(Paragraph(
    "Our headquarters is located at 18 Cross Street, Cross Street Exchange, #08-01, Singapore 048423. "
    "ShopEase operates regional fulfilment centres in Singapore, Malaysia, Indonesia, Thailand, and Vietnam.",
    body_style))

story.append(Paragraph("Mission & Vision", h2_style))
story.append(Paragraph(
    "<b>Mission:</b> To make quality products accessible to everyone in Southeast Asia through technology, "
    "trust, and outstanding service.",
    body_style))
story.append(Paragraph(
    "<b>Vision:</b> To become the most customer-centric e-commerce platform in Southeast Asia by 2030.",
    body_style))

story.append(Paragraph("Core Values", h2_style))
for v in [
    "Customer First – Every decision starts with the customer experience.",
    "Integrity – Transparent pricing, authentic products, honest communication.",
    "Innovation – Continuously improving our platform, logistics, and support.",
    "Sustainability – Committed to eco-friendly packaging and carbon-neutral deliveries by 2027.",
    "Inclusivity – Supporting micro and small businesses to grow through our marketplace.",
]:
    story.append(bullet(v))

story.append(Spacer(1, 0.3*cm))

# ─── 2. Products & Categories ────────────────────────────────────────────────
story += section_header("2. Products & Categories")
story.append(Paragraph(
    "ShopEase hosts over 5 million SKUs across 20+ primary categories. All products sold on the platform "
    "must comply with ShopEase's product authenticity and quality standards.",
    body_style))

cat_data = [
    ["Category", "Examples", "Avg. Delivery Time"],
    ["Electronics", "Smartphones, Laptops, Cameras", "2–4 business days"],
    ["Fashion & Apparel", "Clothing, Shoes, Accessories", "3–5 business days"],
    ["Home & Living", "Furniture, Décor, Appliances", "4–7 business days"],
    ["Health & Beauty", "Skincare, Supplements, Medical", "2–3 business days"],
    ["Sports & Outdoors", "Gym Equipment, Sportswear", "3–5 business days"],
    ["Groceries & Food", "Fresh Produce, Pantry, Beverages", "Same day / Next day"],
    ["Toys & Baby", "Infant Gear, Educational Toys", "2–4 business days"],
    ["Books & Stationery", "Textbooks, Office Supplies", "2–3 business days"],
    ["Automotive", "Car Accessories, Tools", "3–6 business days"],
    ["Digital Goods", "E-vouchers, Software Licenses", "Instant delivery"],
]
cat_table = Table(cat_data, colWidths=[4.5*cm, 6.5*cm, 4.5*cm])
cat_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), BRAND_COLOR),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ACCENT_COLOR]),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("PADDING", (0, 0), (-1, -1), 6),
    ("BOX", (0, 0), (-1, -1), 0.8, DIVIDER_COLOR),
    ("INNERGRID", (0, 0), (-1, -1), 0.4, DIVIDER_COLOR),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(cat_table)
story.append(PageBreak())

# ─── 3. Ordering Process ─────────────────────────────────────────────────────
story += section_header("3. Ordering Process")
steps = [
    ("Browse & Select", "Search or browse the ShopEase catalogue. Use filters to narrow by price, brand, rating, and delivery speed."),
    ("Add to Cart / Buy Now", "Add items to your cart for later checkout or use 'Buy Now' for immediate purchase."),
    ("Checkout", "Review your cart, apply vouchers or loyalty points, and confirm your shipping address."),
    ("Payment", "Choose from multiple payment methods (see Section 4). Orders are confirmed instantly upon successful payment."),
    ("Order Confirmation", "A confirmation email and in-app notification are sent within 5 minutes of order placement."),
    ("Processing & Packing", "The seller or ShopEase Fulfilment Centre processes and packs the order, typically within 24 hours."),
    ("Dispatch & Tracking", "A tracking number is issued via email/SMS. Real-time tracking is available in the ShopEase app."),
    ("Delivery", "Your package is delivered to the specified address. A photo is taken for contactless deliveries."),
    ("Confirmation & Review", "Confirm receipt in the app. Leave a product and seller review to help the community."),
]
for i, (title, desc) in enumerate(steps, 1):
    story.append(Paragraph(f"<b>Step {i}: {title}</b>", h3_style))
    story.append(Paragraph(desc, body_style))

# ─── 4. Payment Policy ───────────────────────────────────────────────────────
story += section_header("4. Payment Policy")
story.append(Paragraph("Accepted Payment Methods", h2_style))
pay_data = [
    ["Payment Method", "Details", "Processing Time"],
    ["Credit / Debit Card", "Visa, Mastercard, Amex", "Instant"],
    ["PayNow / PayLah!", "Singapore bank-linked instant transfer", "Instant"],
    ["GrabPay", "Grab e-wallet", "Instant"],
    ["ShopEase Wallet", "Preloaded e-wallet with cashback", "Instant"],
    ["Bank Transfer", "Manual transfer (selected banks)", "1–2 business days"],
    ["Buy Now Pay Later", "Atome, Rely, Hoolah (0% interest)", "Instant (subject to approval)"],
    ["ShopEase Coins", "Loyalty coins (up to 10% of order value)", "Instant"],
    ["Corporate Invoice", "Net-30 terms for verified businesses", "Purchase Order basis"],
]
pay_table = Table(pay_data, colWidths=[4.5*cm, 7*cm, 4*cm])
pay_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), BRAND_COLOR),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ACCENT_COLOR]),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("PADDING", (0, 0), (-1, -1), 6),
    ("BOX", (0, 0), (-1, -1), 0.8, DIVIDER_COLOR),
    ("INNERGRID", (0, 0), (-1, -1), 0.4, DIVIDER_COLOR),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(pay_table)
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("Billing & Invoice", h2_style))
for p in [
    "All prices on ShopEase are displayed in Singapore Dollars (SGD) inclusive of GST at the prevailing rate.",
    "An itemised e-invoice is automatically emailed after every successful transaction.",
    "Business customers may request a GST-registered tax invoice from the 'My Orders' section.",
    "ShopEase does not store full card numbers; payment data is encrypted via PCI-DSS Level 1 infrastructure.",
    "In the event of a failed payment, no charge is applied to the customer's account.",
]:
    story.append(bullet(p))
story.append(PageBreak())

# ─── 5. Shipping & Logistics ─────────────────────────────────────────────────
story += section_header("5. Shipping & Logistics")
story.append(Paragraph("Shipping Partners", h2_style))
story.append(Paragraph(
    "ShopEase collaborates with a network of trusted last-mile delivery partners to ensure reliable and timely delivery. "
    "Our logistics ecosystem includes both owned fulfilment centres and third-party courier integrations.",
    body_style))

partners = [
    ["Courier Partner", "Coverage", "Special Capability"],
    ["ShopEase Express", "Singapore (all zones)", "Same-day, 2-hour delivery"],
    ["Ninja Van", "SG, MY, ID, TH, VN, PH", "Real-time tracking, POD"],
    ["J&T Express", "SG, MY, ID, TH, VN", "Cash-on-delivery, bulky items"],
    ["DHL Express", "Worldwide", "International shipping, customs"],
    ["Singpost", "Singapore & 220 countries", "Standard & registered mail"],
    ["Lalamove", "SG, MY, ID, TH, VN, PH", "On-demand, same-hour delivery"],
    ["GrabExpress", "Singapore", "On-demand, motorcycle delivery"],
]
p_table = Table(partners, colWidths=[4.5*cm, 5.5*cm, 5.5*cm])
p_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), BRAND_COLOR),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ACCENT_COLOR]),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("PADDING", (0, 0), (-1, -1), 6),
    ("BOX", (0, 0), (-1, -1), 0.8, DIVIDER_COLOR),
    ("INNERGRID", (0, 0), (-1, -1), 0.4, DIVIDER_COLOR),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(p_table)
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("Delivery Options & Fees", h2_style))
del_data = [
    ["Service", "Delivery Time", "Fee (SGD)"],
    ["ShopEase Standard", "3–5 business days", "Free (orders > S$30)"],
    ["ShopEase Express (Same Day)", "Same day (order by 12pm)", "S$4.99"],
    ["ShopEase Express (Next Day)", "Next business day", "S$2.99"],
    ["2-Hour Delivery", "Within 2 hours", "S$6.99"],
    ["International Standard", "7–14 business days", "From S$9.99"],
    ["International Express", "3–5 business days", "From S$19.99"],
    ["Scheduled Delivery", "Choose date & 2-hr slot", "S$1.99 add-on"],
    ["Click & Collect", "Ready in 2–4 hours", "Free"],
]
d_table = Table(del_data, colWidths=[5.5*cm, 4.5*cm, 5.5*cm])
d_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), BRAND_COLOR),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ACCENT_COLOR]),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("PADDING", (0, 0), (-1, -1), 6),
    ("BOX", (0, 0), (-1, -1), 0.8, DIVIDER_COLOR),
    ("INNERGRID", (0, 0), (-1, -1), 0.4, DIVIDER_COLOR),
]))
story.append(d_table)
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("Fulfilment Centres", h2_style))
story.append(Paragraph(
    "ShopEase operates 6 strategically located Fulfilment Centres (FCs) across Southeast Asia:",
    body_style))
for fc in [
    "Singapore FC1 – Jurong East (Primary Hub, 150,000 sqft, climate-controlled)",
    "Singapore FC2 – Tampines (Secondary Hub, 80,000 sqft)",
    "Malaysia FC – Shah Alam, Selangor (120,000 sqft)",
    "Indonesia FC – Cibitung, West Java (200,000 sqft)",
    "Thailand FC – Samut Prakan, Bangkok (90,000 sqft)",
    "Vietnam FC – Binh Duong Province (75,000 sqft)",
]:
    story.append(bullet(fc))

story.append(Paragraph("Packaging Standards", h2_style))
for p in [
    "All orders are packed in ShopEase-branded, tamper-evident packaging.",
    "Fragile items are wrapped with bubble wrap and marked with 'FRAGILE' labels.",
    "ShopEase uses recycled and biodegradable packaging materials for 70% of its shipments.",
    "Temperature-sensitive products (e.g., certain health supplements, fresh food) are shipped in insulated boxes.",
    "Oversized items (>30kg or >120cm longest side) are handled by our Heavy & Bulky team.",
]:
    story.append(bullet(p))
story.append(PageBreak())

# ─── 6. Refund & Return Policy ───────────────────────────────────────────────
story += section_header("6. Refund & Return Policy")
story.append(Paragraph("Overview", h2_style))
story.append(Paragraph(
    "ShopEase is committed to customer satisfaction. If you are not completely satisfied with your purchase, "
    "we offer a straightforward Return and Refund process as outlined below. Our policy is designed to be "
    "fair to both buyers and sellers.",
    body_style))

story.append(Paragraph("Return Eligibility Window", h2_style))
ret_data = [
    ["Category", "Return Window", "Condition Required"],
    ["Electronics", "7 days from delivery", "Sealed / defective only"],
    ["Fashion & Apparel", "14 days from delivery", "Unworn, tags attached"],
    ["Home & Living", "14 days from delivery", "Unused, original packaging"],
    ["Health & Beauty", "7 days from delivery", "Unopened / defective"],
    ["Groceries & Fresh Food", "24 hours from delivery", "Damaged / wrong item"],
    ["Digital Goods & Vouchers", "Non-returnable", "Defective codes: 48hrs"],
    ["Books & Stationery", "14 days from delivery", "Undamaged, unwritten"],
    ["Customised / Personalised Items", "Non-returnable", "Defective only"],
    ["Automotive Parts", "7 days from delivery", "Unused, original packaging"],
]
r_table = Table(ret_data, colWidths=[5*cm, 4.5*cm, 6*cm])
r_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), BRAND_COLOR),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ACCENT_COLOR]),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("PADDING", (0, 0), (-1, -1), 6),
    ("BOX", (0, 0), (-1, -1), 0.8, DIVIDER_COLOR),
    ("INNERGRID", (0, 0), (-1, -1), 0.4, DIVIDER_COLOR),
]))
story.append(r_table)
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("Valid Reasons for Return / Refund", h2_style))
for r in [
    "Item received is damaged or defective upon arrival.",
    "Item received does not match the product description or photos on the listing.",
    "Wrong item or wrong variant (size, colour, model) was delivered.",
    "Item was not delivered within the estimated delivery window (non-digital goods).",
    "Duplicate charge or accidental double-order processed.",
    "Seller cancelled the order after payment was made.",
    "Product is counterfeit or not as described (escalated to ShopEase Buyer Protection).",
]:
    story.append(bullet(r))

story.append(Paragraph("Non-Returnable Items", h2_style))
story.append(Paragraph(
    "The following items cannot be returned unless they arrive damaged or defective:", body_style))
for r in [
    "Perishable goods (fresh produce, chilled/frozen items) after 24 hours.",
    "Intimates, swimwear, and pierced jewellery for hygiene reasons.",
    "Digital downloads, e-vouchers, and software licenses once activated.",
    "Customised, personalised, or made-to-order products.",
    "Hazardous materials, batteries (standalone), and flammable liquids.",
    "Items explicitly marked 'Final Sale' or 'Non-Returnable' in the product listing.",
]:
    story.append(bullet(r))

story.append(Paragraph("How to Initiate a Return", h2_style))
return_steps = [
    "Log in to your ShopEase account and go to <b>My Orders</b>.",
    "Select the order and click <b>Return / Refund</b> within the eligible return window.",
    "Choose the return reason and upload clear photos of the item (required for defective/damaged claims).",
    "Select your preferred resolution: <b>Refund Only</b>, <b>Return &amp; Refund</b>, or <b>Exchange</b>.",
    "ShopEase will review the request within <b>1–2 business days</b> and provide a decision.",
    "If approved, a prepaid return shipping label is emailed to you at no cost.",
    "Pack the item securely and drop it at any authorised return point or schedule a free pickup.",
    "Once the returned item is inspected, the refund is processed within the timelines below.",
]
for i, s in enumerate(return_steps, 1):
    story.append(Paragraph(f"<b>{i}.</b> {s}", bullet_style))

story.append(Paragraph("Refund Timelines", h2_style))
refund_data = [
    ["Refund Method", "Processing Time"],
    ["ShopEase Wallet (instant credits)", "Within 24 hours of approval"],
    ["Original Credit / Debit Card", "5–10 business days (bank dependent)"],
    ["PayNow / PayLah!", "1–2 business days"],
    ["GrabPay / e-Wallet", "2–3 business days"],
    ["Bank Transfer", "3–5 business days"],
    ["Buy Now Pay Later (BNPL)", "Adjusted in next billing cycle"],
    ["ShopEase Coins", "Within 24 hours of approval"],
]
rf_table = Table(refund_data, colWidths=[7.5*cm, 8*cm])
rf_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), BRAND_COLOR),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ACCENT_COLOR]),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("PADDING", (0, 0), (-1, -1), 6),
    ("BOX", (0, 0), (-1, -1), 0.8, DIVIDER_COLOR),
    ("INNERGRID", (0, 0), (-1, -1), 0.4, DIVIDER_COLOR),
]))
story.append(rf_table)
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph(
    "Note: Refund amounts include original shipping fees only if the return is due to a ShopEase or seller error. "
    "For buyer-initiated returns (e.g., change of mind), original shipping fees are non-refundable.",
    note_style))
story.append(PageBreak())

# ─── 7. Exchange Policy ──────────────────────────────────────────────────────
story += section_header("7. Exchange Policy")
story.append(Paragraph(
    "ShopEase offers a direct exchange service for eligible items. Exchanges are available for a different size, "
    "colour, or variant of the same product, subject to stock availability.",
    body_style))

story.append(Paragraph("Exchange Eligibility", h2_style))
for e in [
    "Exchange requests must be submitted within the return window for the respective category.",
    "The item must be in its original, unused condition with all packaging and tags intact.",
    "Exchange is available for the same product (different size/variant) only. For a different product, initiate a return and repurchase.",
    "Electronics exchanges require a functional test report from a ShopEase-certified technician for defective claims.",
    "Items purchased during flash sales or with promo codes may be exchanged for store credit only.",
]:
    story.append(bullet(e))

story.append(Paragraph("Exchange Process", h2_style))
for i, s in enumerate([
    "Submit exchange request via My Orders > Return/Refund > Exchange.",
    "ShopEase confirms stock availability within 1 business day.",
    "Ship back the original item using the provided prepaid label.",
    "Upon receipt and inspection, the replacement is dispatched within 2 business days.",
], 1):
    story.append(Paragraph(f"<b>{i}.</b> {s}", bullet_style))

# ─── 8. Cancellation Policy ──────────────────────────────────────────────────
story += section_header("8. Cancellation Policy")
story.append(Paragraph("Buyer-Initiated Cancellation", h2_style))
canc_data = [
    ["Order Status", "Cancellation Allowed?", "Refund"],
    ["Payment Pending", "Yes – cancel anytime", "Full refund (auto)"],
    ["Payment Confirmed (within 1hr)", "Yes – self-service via app", "Full refund"],
    ["Processing / Packing", "Yes – request within 30 min", "Full refund if approved"],
    ["Shipped / Out for Delivery", "No – initiate return after delivery", "Return refund policy applies"],
    ["Delivered", "No – initiate return", "Return refund policy applies"],
]
c_table = Table(canc_data, colWidths=[4.5*cm, 5*cm, 6*cm])
c_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), BRAND_COLOR),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ACCENT_COLOR]),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("PADDING", (0, 0), (-1, -1), 6),
    ("BOX", (0, 0), (-1, -1), 0.8, DIVIDER_COLOR),
    ("INNERGRID", (0, 0), (-1, -1), 0.4, DIVIDER_COLOR),
]))
story.append(c_table)
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("Seller-Initiated Cancellation", h2_style))
story.append(Paragraph(
    "If a seller cancels your order after payment, you will receive a full refund including shipping fees "
    "within 24 hours to your ShopEase Wallet or within the standard refund timeline for other methods. "
    "Repeated seller cancellations are penalised under ShopEase's Seller Performance Policy.",
    body_style))
story.append(PageBreak())

# ─── 9. Customer Support ─────────────────────────────────────────────────────
story += section_header("9. Customer Support")
story.append(Paragraph("Support Channels", h2_style))
supp_data = [
    ["Channel", "Availability", "Response Time", "Best For"],
    ["Live Chat (App & Web)", "24 / 7", "< 2 minutes", "Order issues, quick queries"],
    ["Email Support", "24 / 7", "< 4 hours", "Detailed complaints, documentation"],
    ["Phone Hotline", "Mon–Fri 8am–10pm", "< 5 minutes wait", "Urgent / complex issues"],
    ["WhatsApp", "Mon–Sun 8am–10pm", "< 15 minutes", "Order tracking, returns"],
    ["Social Media DM", "Mon–Fri 9am–6pm", "< 2 hours", "General enquiries"],
    ["In-App Help Centre", "24 / 7 (self-service)", "Instant", "FAQs, guides, policies"],
    ["Community Forum", "24 / 7 (peer support)", "Varies", "Tips, product reviews"],
]
s_table = Table(supp_data, colWidths=[3.8*cm, 3.2*cm, 3.2*cm, 5.3*cm])
s_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), BRAND_COLOR),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ACCENT_COLOR]),
    ("FONTSIZE", (0, 0), (-1, -1), 8.5),
    ("PADDING", (0, 0), (-1, -1), 5),
    ("BOX", (0, 0), (-1, -1), 0.8, DIVIDER_COLOR),
    ("INNERGRID", (0, 0), (-1, -1), 0.4, DIVIDER_COLOR),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(s_table)
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("Contact Details", h2_style))
contact_info = [
    ("Customer Service Hotline", "+65 6789 1234"),
    ("Customer Service Email", "support@shopease.com"),
    ("Business / Corporate Queries", "corporate@shopease.com"),
    ("Seller Support", "seller.support@shopease.com"),
    ("Press & Media", "media@shopease.com"),
    ("Complaints & Escalation", "escalations@shopease.com"),
    ("Headquarters Address", "18 Cross Street, Cross Street Exchange, #08-01, Singapore 048423"),
]
for label, val in contact_info:
    story.append(Paragraph(f"<b>{label}:</b> {val}", body_style))

story.append(Paragraph("Escalation Process", h2_style))
for i, s in enumerate([
    "Contact customer support through any channel and receive a Case ID.",
    "If unresolved within 48 hours, request escalation to a Senior Support Specialist.",
    "Unresolved cases after 72 hours are escalated to the ShopEase Resolution Team.",
    "For disputes involving seller fraud, counterfeit, or safety issues, ShopEase Buyer Protection is activated automatically.",
    "Persistent unresolved disputes may be referred to the Singapore Mediation Centre (for Singapore-based customers).",
], 1):
    story.append(Paragraph(f"<b>{i}.</b> {s}", bullet_style))
story.append(PageBreak())

# ─── 10. Privacy Policy ──────────────────────────────────────────────────────
story += section_header("10. Privacy Policy")
story.append(Paragraph("Data We Collect", h2_style))
for d in [
    "<b>Account Data:</b> Name, email, phone number, date of birth, and profile photo.",
    "<b>Transaction Data:</b> Order history, payment method details (tokenised), billing and shipping addresses.",
    "<b>Usage Data:</b> Browsing history, search queries, click behaviour, and device information.",
    "<b>Location Data:</b> Approximate or precise location (if permission granted) for delivery and localisation.",
    "<b>Communications Data:</b> Chat messages with sellers, support tickets, and reviews.",
    "<b>Third-Party Data:</b> Data from linked social accounts (Facebook, Google) used for login or promotions.",
]:
    story.append(bullet(d))

story.append(Paragraph("How We Use Your Data", h2_style))
for d in [
    "To process and fulfil your orders and communicate order status.",
    "To personalise your shopping experience and product recommendations.",
    "To verify your identity and prevent fraud.",
    "To comply with legal and regulatory obligations.",
    "To improve our platform, logistics, and customer service.",
    "To send you promotional communications (with your consent; unsubscribe anytime).",
]:
    story.append(bullet(d))

story.append(Paragraph("Data Retention & Rights", h2_style))
story.append(Paragraph(
    "ShopEase retains personal data for as long as necessary to provide services and comply with legal obligations "
    "(typically 5–7 years for transaction records). You have the right to access, correct, port, or delete your data "
    "at any time through the Privacy Settings page in your account, or by emailing privacy@shopease.com.",
    body_style))
story.append(Paragraph(
    "ShopEase complies with Singapore's Personal Data Protection Act (PDPA) 2012, and applicable data protection "
    "regulations in all operating countries including Malaysia's PDPA, Indonesia's PDP Law, and Thailand's PDPA.",
    body_style))

# ─── 11. Terms & Conditions ──────────────────────────────────────────────────
story += section_header("11. Terms & Conditions")
story.append(Paragraph("User Eligibility", h2_style))
story.append(Paragraph(
    "ShopEase services are available to users aged 18 and above. Users aged 13–17 may use the platform with "
    "verifiable parental or guardian consent. Accounts suspected of being used by minors without consent will be suspended.",
    body_style))

story.append(Paragraph("Prohibited Activities", h2_style))
for p in [
    "Listing counterfeit, recalled, or illegal products.",
    "Misrepresenting product descriptions, images, or specifications.",
    "Creating fake reviews or engaging in review manipulation.",
    "Using bots, scrapers, or automated tools without written permission.",
    "Circumventing ShopEase's payment or logistics systems for off-platform transactions.",
    "Harassment, threats, or abusive behaviour towards other users, sellers, or ShopEase staff.",
    "Account sharing or selling ShopEase accounts.",
]:
    story.append(bullet(p))

story.append(Paragraph("Intellectual Property", h2_style))
story.append(Paragraph(
    "All content on the ShopEase platform, including logos, designs, text, graphics, and software, is the property "
    "of ShopEase Inc. or its licensors and is protected by applicable intellectual property laws. "
    "Unauthorised reproduction or redistribution is strictly prohibited.",
    body_style))

story.append(Paragraph("Limitation of Liability", h2_style))
story.append(Paragraph(
    "ShopEase acts as an intermediary marketplace and is not liable for the quality, safety, or legality of items "
    "listed by third-party sellers, except where ShopEase Fulfilment is used. Our maximum liability to any customer "
    "in connection with any order shall not exceed the total amount paid for that order.",
    body_style))
story.append(PageBreak())

# ─── 12. Seller / Vendor Policy ──────────────────────────────────────────────
story += section_header("12. Seller / Vendor Policy")
story.append(Paragraph("Seller Onboarding Requirements", h2_style))
for r in [
    "Valid business registration (ACRA for Singapore sellers, equivalent for other countries).",
    "Bank account in the registered business name.",
    "At least one identity verification document (NRIC/Passport for sole proprietors).",
    "Product catalogue compliant with ShopEase listing standards.",
    "Agreement to ShopEase Seller Terms, Commission Schedule, and Shipping SLAs.",
]:
    story.append(bullet(r))

story.append(Paragraph("Commission & Fee Structure", h2_style))
fee_data = [
    ["Category", "Commission Rate", "Payment Processing Fee"],
    ["Electronics", "3%–5%", "1.5%"],
    ["Fashion & Apparel", "6%–10%", "1.5%"],
    ["Home & Living", "5%–8%", "1.5%"],
    ["Health & Beauty", "7%–10%", "1.5%"],
    ["Groceries", "4%–6%", "1.5%"],
    ["All Other Categories", "5%–8%", "1.5%"],
]
f_table = Table(fee_data, colWidths=[5*cm, 5*cm, 5.5*cm])
f_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), BRAND_COLOR),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ACCENT_COLOR]),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("PADDING", (0, 0), (-1, -1), 6),
    ("BOX", (0, 0), (-1, -1), 0.8, DIVIDER_COLOR),
    ("INNERGRID", (0, 0), (-1, -1), 0.4, DIVIDER_COLOR),
]))
story.append(f_table)
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph(
    "Seller payouts are processed every Monday for orders completed and not disputed in the preceding week.",
    note_style))

# ─── 13. Loyalty Program ─────────────────────────────────────────────────────
story += section_header("13. Loyalty Program – ShopEase Rewards")
story.append(Paragraph(
    "ShopEase Rewards is our tiered loyalty programme that lets customers earn and redeem ShopEase Coins on every purchase.",
    body_style))
tier_data = [
    ["Tier", "Annual Spend", "Coins Earning Rate", "Benefits"],
    ["Silver", "S$0–S$499", "1 coin per S$1", "Birthday bonus, free shipping (x2/month)"],
    ["Gold", "S$500–S$1,999", "1.5 coins per S$1", "Priority support, free shipping (unlimited)"],
    ["Platinum", "S$2,000–S$4,999", "2 coins per S$1", "Early access to sales, dedicated agent"],
    ["Diamond", "S$5,000+", "3 coins per S$1", "VIP events, free express delivery, personal shopper"],
]
t_table = Table(tier_data, colWidths=[2.5*cm, 3*cm, 3.5*cm, 6.5*cm])
t_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), BRAND_COLOR),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ACCENT_COLOR]),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("PADDING", (0, 0), (-1, -1), 6),
    ("BOX", (0, 0), (-1, -1), 0.8, DIVIDER_COLOR),
    ("INNERGRID", (0, 0), (-1, -1), 0.4, DIVIDER_COLOR),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(t_table)
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph(
    "1 ShopEase Coin = S$0.01. Coins can be used to offset up to 10% of any order value. "
    "Coins expire 12 months after the last account activity.",
    note_style))
story.append(PageBreak())

# ─── 14. FAQs ────────────────────────────────────────────────────────────────
story += section_header("14. Frequently Asked Questions (FAQs)")
faqs = [
    ("How do I track my order?",
     "Once your order is dispatched, you will receive an SMS and email with a tracking number. You can track "
     "your order in real-time via the ShopEase app under My Orders > Track Package, or directly on the courier's website."),
    ("What do I do if my item arrives damaged?",
     "Do not discard the packaging. Take clear photos of the damaged item and packaging, then submit a Return/Refund "
     "request within 48 hours of delivery via My Orders. Select 'Item Damaged' as the reason and upload your photos. "
     "Approved claims receive a full refund or replacement at no extra cost."),
    ("Can I change my delivery address after placing an order?",
     "Address changes are only possible before the order is packed. Go to My Orders > Order Details > Edit Address. "
     "If the order is already packed or shipped, contact our live chat support immediately. Additional charges may apply "
     "for rerouting."),
    ("How do I apply a voucher code?",
     "At checkout, click 'Apply Voucher / Promo Code' and enter your code. Valid vouchers will be applied automatically "
     "to the eligible items. Only one voucher code can be used per order, but it can be combined with ShopEase Coins."),
    ("Is my payment information secure?",
     "Yes. ShopEase uses PCI-DSS Level 1 compliant payment infrastructure. We never store your full card number. "
     "All transactions are encrypted using 256-bit SSL. We also support two-factor authentication (2FA) for account security."),
    ("What is ShopEase Buyer Protection?",
     "ShopEase Buyer Protection guarantees a full refund if: your order never arrives, the item is significantly "
     "different from the listing, or the item is counterfeit. Protection is automatically active on all orders and "
     "you can open a claim within 15 days of the estimated delivery date."),
    ("How long does it take to process a return?",
     "Once we receive your returned item, inspection takes 1–2 business days. Refunds are processed immediately upon "
     "approval. Depending on your payment method, refunds reflect in 24 hours (ShopEase Wallet) to 10 business days (bank card)."),
    ("Can I return an international order?",
     "Yes. For cross-border orders, submit your return request via the app. A prepaid international return label will "
     "be emailed to you. International returns may take 7–14 business days to reach our warehouse. Customs duties paid "
     "on original delivery are non-refundable."),
    ("How do I become a seller on ShopEase?",
     "Visit seller.shopease.com and click 'Register as Seller'. Complete the KYC process, upload required documents, "
     "and set up your store. Onboarding typically takes 2–3 business days. Our Seller Success team will guide you through "
     "your first 30 days."),
    ("What happens if the seller does not respond to my return request?",
     "Sellers must respond to return requests within 2 business days. If they do not respond, ShopEase will auto-approve "
     "your return and process the refund on behalf of the seller. The seller's account is penalised under the Seller Performance Policy."),
    ("Does ShopEase offer price matching?",
     "ShopEase does not offer a formal price-match guarantee. However, our Price Alert feature lets you set a target "
     "price for any item and notifies you when it drops to that level. During our ShopEase Sale events, prices are "
     "often at their lowest."),
    ("How do I delete my ShopEase account?",
     "Go to Account Settings > Privacy > Delete My Account. All personal data will be erased within 30 days, except "
     "records legally required to be retained (e.g., transaction records for tax purposes). Outstanding orders, "
     "disputes, or balances must be resolved before deletion."),
]
for q, a in faqs:
    story.append(Paragraph(q, h3_style))
    story.append(Paragraph(a, body_style))
    story.append(Spacer(1, 0.1*cm))

story.append(PageBreak())

# ─── Footer Page ─────────────────────────────────────────────────────────────
story.append(Spacer(1, 2*cm))
story.append(Paragraph("ShopEase Inc.", title_style))
story.append(Paragraph("Official Company Knowledge Base Document", subtitle_style))
story.append(Spacer(1, 0.5*cm))
story.append(divider())
story.append(Paragraph(
    "This document is intended for internal use, customer support teams, and RAG (Retrieval Augmented Generation) "
    "knowledge base ingestion. Content is subject to change. For the latest version, visit help.shopease.com.",
    note_style))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(f"© {datetime.today().year} ShopEase Inc. All Rights Reserved. | Singapore UEN: 201823456K", note_style))

doc.build(story)
print("PDF generated successfully.")