import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";
import {
    Form,
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { ArrowLeft, ArrowRight, Loader2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

const intakeSchema = z.object({
    studentName: z.string().trim().min(1, "Name is required").max(100, "Name must be less than 100 characters"),
    email: z.string().trim().email("Please enter a valid email").max(255, "Email must be less than 255 characters"),
    graduationYear: z.string().min(1, "Please select your graduation year"),
    selectedPrograms: z.array(z.string()).min(1, "Please select at least one program"),
    applicationDeadline: z.string().optional(),
});

type IntakeFormData = z.infer<typeof intakeSchema>;

const programOptions = [
    { id: "cs-uoft", label: "Computer Science - University of Toronto", category: "computer-science" },
    { id: "se-waterloo", label: "Software Engineering - University of Waterloo", category: "computer-science" },
    { id: "health-mcmaster", label: "Health Sciences - McMaster University", category: "health-sciences" },
    { id: "commerce-queens", label: "Commerce - Queen's University", category: "business" },
    { id: "eng-uoft", label: "Engineering Science - University of Toronto", category: "engineering" },
    { id: "cs-waterloo", label: "Computer Science - University of Waterloo", category: "computer-science" },
    { id: "bba-laurier", label: "BBA - Wilfrid Laurier University", category: "business" },
    { id: "life-sci-mcmaster", label: "Life Sciences - McMaster University", category: "health-sciences" },
];

const Intake = () => {
    const navigate = useNavigate();
    const { toast } = useToast();
    const [isSubmitting, setIsSubmitting] = useState(false);

    const form = useForm<IntakeFormData>({
        resolver: zodResolver(intakeSchema),
        defaultValues: {
            studentName: "",
            email: "",
            graduationYear: "",
            selectedPrograms: [],
            applicationDeadline: "",
        },
    });

    const onSubmit = async (data: IntakeFormData) => {
        setIsSubmitting(true);

        // Simulate roadmap generation
        await new Promise((resolve) => setTimeout(resolve, 1500));

        // Store in localStorage for demo purposes
        const roadmapId = `roadmap-${Date.now()}`;
        const newRoadmap = {
            id: roadmapId,
            studentName: data.studentName,
            email: data.email,
            graduationYear: data.graduationYear,
            selectedPrograms: data.selectedPrograms,
            createdAt: new Date().toISOString(),
        };

        // Get existing roadmaps or create empty array
        const existingRoadmaps = JSON.parse(localStorage.getItem("userRoadmaps") || "[]");
        existingRoadmaps.push(newRoadmap);
        localStorage.setItem("userRoadmaps", JSON.stringify(existingRoadmaps));
        localStorage.setItem("currentRoadmap", JSON.stringify(newRoadmap));

        setIsSubmitting(false);

        toast({
            title: "Roadmap Created!",
            description: "Your personalized application roadmap is ready.",
        });

        navigate("/dashboard");
    };

    return (
        <div className="min-h-screen bg-background py-12">
            <div className="container mx-auto px-4 max-w-2xl">
                <Button
                    variant="ghost"
                    className="mb-6 gap-2"
                    onClick={() => navigate("/")}
                >
                    <ArrowLeft className="h-4 w-4" />
                    Back to Home
                </Button>

                <Card>
                    <CardHeader>
                        <CardTitle className="text-2xl">Create Your Application Roadmap</CardTitle>
                        <CardDescription>
                            Tell us about yourself and your goals. We'll generate a personalized
                            roadmap to guide you through your university applications.
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        <Form {...form}>
                            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                                {/* Student Name */}
                                <FormField
                                    control={form.control}
                                    name="studentName"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Your Name</FormLabel>
                                            <FormControl>
                                                <Input placeholder="Enter your full name" {...field} />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />

                                {/* Email */}
                                <FormField
                                    control={form.control}
                                    name="email"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Email Address</FormLabel>
                                            <FormControl>
                                                <Input type="email" placeholder="your.email@example.com" {...field} />
                                            </FormControl>
                                            <FormDescription>
                                                We'll send deadline reminders to this email
                                            </FormDescription>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />

                                {/* Graduation Year */}
                                <FormField
                                    control={form.control}
                                    name="graduationYear"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Expected High School Graduation</FormLabel>
                                            <Select onValueChange={field.onChange} defaultValue={field.value}>
                                                <FormControl>
                                                    <SelectTrigger>
                                                        <SelectValue placeholder="Select your graduation year" />
                                                    </SelectTrigger>
                                                </FormControl>
                                                <SelectContent>
                                                    <SelectItem value="2025">2025</SelectItem>
                                                    <SelectItem value="2026">2026</SelectItem>
                                                    <SelectItem value="2027">2027</SelectItem>
                                                    <SelectItem value="2028">2028</SelectItem>
                                                </SelectContent>
                                            </Select>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />

                                {/* Program Selection */}
                                <FormField
                                    control={form.control}
                                    name="selectedPrograms"
                                    render={() => (
                                        <FormItem>
                                            <div className="mb-4">
                                                <FormLabel className="text-base">Programs of Interest</FormLabel>
                                                <FormDescription>
                                                    Select all programs you're interested in applying to
                                                </FormDescription>
                                            </div>
                                            <div className="grid gap-3">
                                                {programOptions.map((program) => (
                                                    <FormField
                                                        key={program.id}
                                                        control={form.control}
                                                        name="selectedPrograms"
                                                        render={({ field }) => {
                                                            return (
                                                                <FormItem
                                                                    key={program.id}
                                                                    className="flex flex-row items-start space-x-3 space-y-0 rounded-md border border-border p-4 hover:bg-muted/50 transition-colors"
                                                                >
                                                                    <FormControl>
                                                                        <Checkbox
                                                                            checked={field.value?.includes(program.id)}
                                                                            onCheckedChange={(checked) => {
                                                                                return checked
                                                                                    ? field.onChange([...field.value, program.id])
                                                                                    : field.onChange(
                                                                                        field.value?.filter(
                                                                                            (value) => value !== program.id
                                                                                        )
                                                                                    );
                                                                            }}
                                                                        />
                                                                    </FormControl>
                                                                    <FormLabel className="font-normal cursor-pointer flex-1">
                                                                        {program.label}
                                                                    </FormLabel>
                                                                </FormItem>
                                                            );
                                                        }}
                                                    />
                                                ))}
                                            </div>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />

                                <Button type="submit" className="w-full gap-2" disabled={isSubmitting}>
                                    {isSubmitting ? (
                                        <>
                                            <Loader2 className="h-4 w-4 animate-spin" />
                                            Creating Your Roadmap...
                                        </>
                                    ) : (
                                        <>
                                            Generate My Roadmap
                                            <ArrowRight className="h-4 w-4" />
                                        </>
                                    )}
                                </Button>
                            </form>
                        </Form>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
};

export default Intake;
