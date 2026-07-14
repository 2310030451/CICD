"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { CreditCard, Zap, FileText, Eye, CheckCircle, XCircle, Loader2, Crown, Star, Building, Rocket } from "lucide-react";

export default function SubscriptionPage() {
  const [subscription, setSubscription] = useState<any>(null);
  const [usage, setUsage] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [upgrading, setUpgrading] = useState(false);

  const plans = [
    {
      id: "free",
      name: "Free",
      icon: Star,
      price: "",
      period: "forever",
      features: ["100 AI credits", "10 documents", "20 Vision AI uses", "Basic support"],
      limits: { ai_credits: 100, documents: 10, vision_ai: 20 }
    },
    {
      id: "student_pro",
      name: "Student Pro",
      icon: Crown,
      price: ".99",
      period: "month",
      features: ["1,000 AI credits", "100 documents", "200 Vision AI uses", "Priority support", "All AI agents"],
      limits: { ai_credits: 1000, documents: 100, vision_ai: 200 }
    },
    {
      id: "premium",
      name: "Premium",
      icon: Zap,
      price: ".99",
      period: "month",
      features: ["5,000 AI credits", "500 documents", "1,000 Vision AI uses", "24/7 support", "Advanced analytics", "All AI agents"],
      limits: { ai_credits: 5000, documents: 500, vision_ai: 1000 }
    },
    {
      id: "institution",
      name: "Institution",
      icon: Building,
      price: ".99",
      period: "month",
      features: ["20,000 AI credits", "2,000 documents", "5,000 Vision AI uses", "Dedicated support", "Custom integrations", "Teacher dashboard"],
      limits: { ai_credits: 20000, documents: 2000, vision_ai: 5000 }
    },
    {
      id: "enterprise",
      name: "Enterprise",
      icon: Rocket,
      price: "Custom",
      period: "contact",
      features: ["Unlimited AI credits", "Unlimited documents", "Unlimited Vision AI", "SLA guarantee", "On-premise deployment", "Full API access"],
      limits: { ai_credits: 100000, documents: 10000, vision_ai: 25000 }
    }
  ];

  useEffect(() => {
    fetchSubscription();
    fetchUsage();
  }, []);

  const fetchSubscription = async () => {
    try {
      const response = await fetch(${process.env.NEXT_PUBLIC_API_URL}/api/v1/subscriptions/my-subscription, {
        headers: {
          Authorization: Bearer ,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setSubscription(data);
      }
    } catch (error) {
      console.error("Failed to fetch subscription:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchUsage = async () => {
    try {
      const response = await fetch(${process.env.NEXT_PUBLIC_API_URL}/api/v1/subscriptions/usage, {
        headers: {
          Authorization: Bearer ,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setUsage(data);
      }
    } catch (error) {
      console.error("Failed to fetch usage:", error);
    }
  };

  const handleUpgrade = async (planId: string) => {
    setUpgrading(true);
    try {
      const response = await fetch(${process.env.NEXT_PUBLIC_API_URL}/api/v1/subscriptions/create-checkout-session?plan=, {
        method: "POST",
        headers: {
          Authorization: Bearer ,
        },
      });
      if (response.ok) {
        const data = await response.json();
        window.location.href = data.checkout_url;
      }
    } catch (error) {
      console.error("Failed to create checkout session:", error);
    } finally {
      setUpgrading(false);
    }
  };

  const handleCancel = async () => {
    if (!confirm("Are you sure you want to cancel your subscription?")) return;
    
    try {
      const response = await fetch(${process.env.NEXT_PUBLIC_API_URL}/api/v1/subscriptions/cancel, {
        method: "POST",
        headers: {
          Authorization: Bearer ,
        },
      });
      if (response.ok) {
        fetchSubscription();
      }
    } catch (error) {
      console.error("Failed to cancel subscription:", error);
    }
  };

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-muted rounded w-1/3" />
          <div className="h-4 bg-muted rounded w-1/2" />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-48 bg-muted rounded" />
            ))}
          </div>
        </div>
      </div>
    );
  }

  const currentPlan = plans.find(p => p.id === subscription?.plan);

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Subscription</h1>
        <p className="text-muted-foreground">Manage your subscription and usage</p>
      </div>

      {/* Current Plan */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            {currentPlan && <currentPlan.icon className="h-5 w-5" />}
            Current Plan: {currentPlan?.name || "Free"}
          </CardTitle>
          <CardDescription>
            Status: <Badge variant={subscription?.status === "active" ? "default" : "secondary"}>{subscription?.status}</Badge>
          </CardDescription>
        </CardHeader>
        <CardContent>
          {subscription?.plan !== "free" && (
            <Button variant="destructive" onClick={handleCancel}>
              Cancel Subscription
            </Button>
          )}
        </CardContent>
      </Card>

      {/* Usage Statistics */}
      {usage && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Zap className="h-5 w-5" />
                AI Credits
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <Progress value={(usage.ai_credits.used / usage.ai_credits.limit) * 100} />
                <p className="text-sm text-muted-foreground">
                  {usage.ai_credits.used} / {usage.ai_credits.limit} credits
                </p>
                <p className="text-sm font-medium">{usage.ai_credits.remaining} remaining</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="h-5 w-5" />
                Documents
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <Progress value={(usage.documents.used / usage.documents.limit) * 100} />
                <p className="text-sm text-muted-foreground">
                  {usage.documents.used} / {usage.documents.limit} documents
                </p>
                <p className="text-sm font-medium">{usage.documents.remaining} remaining</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Eye className="h-5 w-5" />
                Vision AI
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <Progress value={(usage.vision_ai.used / usage.vision_ai.limit) * 100} />
                <p className="text-sm text-muted-foreground">
                  {usage.vision_ai.used} / {usage.vision_ai.limit} uses
                </p>
                <p className="text-sm font-medium">{usage.vision_ai.remaining} remaining</p>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Available Plans */}
      <div>
        <h2 className="text-2xl font-bold mb-4">Upgrade Your Plan</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {plans.filter(p => p.id !== subscription?.plan).map((plan) => (
            <Card key={plan.id} className={plan.id === "premium" ? "border-primary" : ""}>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <plan.icon className="h-5 w-5" />
                  {plan.name}
                </CardTitle>
                <CardDescription>
                  {plan.price} / {plan.period}
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <ul className="space-y-2">
                  {plan.features.map((feature, index) => (
                    <li key={index} className="flex items-center gap-2 text-sm">
                      <CheckCircle className="h-4 w-4 text-green-500" />
                      {feature}
                    </li>
                  ))}
                </ul>
                <Button 
                  className="w-full" 
                  onClick={() => handleUpgrade(plan.id)}
                  disabled={upgrading}
                >
                  {upgrading ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : null}
                  Upgrade to {plan.name}
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Billing Information */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <CreditCard className="h-5 w-5" />
            Billing Information
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            Your subscription will be billed monthly. You can cancel at any time.
            For enterprise plans, contact sales for custom pricing.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
