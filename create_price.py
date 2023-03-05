import stripe
stripe.api_key = "sk_test_51MhSbTIYyN8YHp26pjmeK0q5ul2WW4kt9lIYDGfZtk2SQvJZ4vBS3giLxm2ElijCVHSKudMVjeMwIKgZV73pdh4s00jDDbO2wW"

starter_subscription = stripe.Product.create(
  name="Starter Subscription",
  description="$12/Month subscription",
)

starter_subscription_price = stripe.Price.create(
  unit_amount=1200,
  currency="usd",
  recurring={"interval": "month"},
  product=starter_subscription['id'],
)

# Save these identifiers
print(f"Success! Here is your starter subscription product id: {starter_subscription.id}")
print(f"Success! Here is your starter subscription price id: {starter_subscription_price.id}")