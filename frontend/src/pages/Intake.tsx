import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useForm, useFieldArray } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
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
import { MultiSelect, Option } from "@/components/ui/multi-select";
import { ArrowLeft, ArrowRight, Loader2, Plus, Trash2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

const extraCurricularSchema = z.object({
    name: z.string().min(1, "Activity name is required"),
    leadership_level: z.number().min(1, "Leadership level must be at least 1").max(4, "Leadership level must be at most 4"),
});

const courseTakenSchema = z.object({
    course: z.string().min(1, "Please select a course"),
    grade: z.number().min(0, "Grade must be at least 0").max(100, "Grade must be at most 100"),
});

const intakeSchema = z.object({
    name: z.string().trim().min(1, "Name is required").max(100, "Name must be less than 100 characters"),
    email: z.string().trim().email("Please enter a valid email").max(255, "Email must be less than 255 characters"),
    grade: z.string().min(1, "Please select your current grade level"),
    extra_curriculars: z.array(extraCurricularSchema).min(0),
    interests: z.array(z.string()).min(1, "Please select at least one interest"),
    courses_taken: z.array(courseTakenSchema).min(1, "Please add at least one course with a grade"),
});

type IntakeFormData = z.infer<typeof intakeSchema>;

const interestOptions: Option[] = [
    { value: "Computer Science", label: "Computer Science" },
    { value: "Software Engineering", label: "Software Engineering" },
    { value: "Electrical Engineering", label: "Electrical Engineering" },
    { value: "Mechanical Engineering", label: "Mechanical Engineering" },
    { value: "Civil Engineering", label: "Civil Engineering" },
    { value: "Chemical Engineering", label: "Chemical Engineering" },
    { value: "Aerospace Engineering", label: "Aerospace Engineering" },
    { value: "Biomedical Engineering", label: "Biomedical Engineering" },
    { value: "Industrial Engineering", label: "Industrial Engineering" },
    { value: "Materials Engineering", label: "Materials Engineering" },
    { value: "Systems Engineering", label: "Systems Engineering" },
    { value: "Environmental Engineering", label: "Environmental Engineering" },
    { value: "Computer Engineering", label: "Computer Engineering" },
    { value: "Robotics Engineering", label: "Robotics Engineering" },
    { value: "Mechatronics Engineering", label: "Mechatronics Engineering" },
    { value: "Engineering Physics", label: "Engineering Physics" },
    { value: "Physics", label: "Physics" },
    { value: "Mathematics", label: "Mathematics" },
    { value: "Chemistry", label: "Chemistry" },
];

const courseOptions: Option[] = [
    { value: "grade-9-math", label: "Grade 9 Mathematics" },
    { value: "grade-9-english", label: "Grade 9 English" },
    { value: "grade-9-science", label: "Grade 9 Science" },
    { value: "grade-9-technology", label: "Grade 9 Technology" },
    { value: "grade-10-math", label: "Grade 10 Mathematics" },
    { value: "grade-10-english", label: "Grade 10 English" },
    { value: "grade-10-science", label: "Grade 10 Science" },
    { value: "grade-10-technology", label: "Grade 10 Technology" },
    { value: "grade-11-functions", label: "Grade 11 Functions" },
    { value: "grade-11-english", label: "Grade 11 English" },
    { value: "grade-11-chemistry", label: "Grade 11 Chemistry" },
    { value: "grade-11-physics", label: "Grade 11 Physics" },
    { value: "grade-11-computer-science", label: "Grade 11 Computer Science" },
    { value: "grade-11-engineering", label: "Grade 11 Engineering" },
    { value: "grade-11-technology", label: "Grade 11 Technology" },
    { value: "grade-12-advanced-functions", label: "Grade 12 Advanced Functions" },
    { value: "grade-12-calculus", label: "Grade 12 Calculus" },
    { value: "grade-12-english", label: "Grade 12 English" },
    { value: "grade-12-chemistry", label: "Grade 12 Chemistry" },
    { value: "grade-12-physics", label: "Grade 12 Physics" },
    { value: "grade-12-computer-science", label: "Grade 12 Computer Science" },
    { value: "grade-12-data-management", label: "Grade 12 Data Management" },
    { value: "grade-12-engineering", label: "Grade 12 Engineering" },
    { value: "grade-12-technology", label: "Grade 12 Technology" },
];

const Intake = () => {
    const navigate = useNavigate();
    const { toast } = useToast();
    const [isSubmitting, setIsSubmitting] = useState(false);

    const form = useForm<IntakeFormData>({
        resolver: zodResolver(intakeSchema),
        defaultValues: {
            name: "",
            email: "",
            grade: "",
            extra_curriculars: [],
            interests: [],
            courses_taken: [],
        },
    });

    const { fields: extraCurricularFields, append: appendExtraCurricular, remove: removeExtraCurricular } = useFieldArray({
        control: form.control,
        name: "extra_curriculars",
    });

    const { fields: courseFields, append: appendCourse, remove: removeCourse } = useFieldArray({
        control: form.control,
        name: "courses_taken",
    });

    const onSubmit = async (data: IntakeFormData) => {
        setIsSubmitting(true);

        // Simulate roadmap generation
        await new Promise((resolve) => setTimeout(resolve, 1500));

        // Transform data to match the required JSON schema
        const studentProfile = {
            name: data.name,
            email: data.email,
            grade: data.grade,
            extra_curriculars: data.extra_curriculars.map((ec) => ({
                name: ec.name,
                leadership_level: ec.leadership_level,
            })),
            interests: data.interests,
            courses_taken: data.courses_taken.map((course) => ({
                course: course.course,
                grade: course.grade,
            })),
        };

        // Store in localStorage for demo purposes
        const roadmapId = `roadmap-${Date.now()}`;
        const newRoadmap = {
            id: roadmapId,
            student_profile: studentProfile,
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
                                {/* Name */}
                                <FormField
                                    control={form.control}
                                    name="name"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>What is your full name?</FormLabel>
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
                                            <FormLabel>What is your email address?</FormLabel>
                                            <FormControl>
                                                <Input type="email" placeholder="your.email@example.com" {...field} />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />

                                {/* Grade */}
                                <FormField
                                    control={form.control}
                                    name="grade"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>What is your current grade level?</FormLabel>
                                            <Select onValueChange={field.onChange} value={field.value}>
                                                <FormControl>
                                                    <SelectTrigger>
                                                        <SelectValue placeholder="Select your grade level" />
                                                    </SelectTrigger>
                                                </FormControl>
                                                <SelectContent>
                                                    <SelectItem value="Grade 9">Grade 9</SelectItem>
                                                    <SelectItem value="Grade 10">Grade 10</SelectItem>
                                                    <SelectItem value="Grade 11">Grade 11</SelectItem>
                                                    <SelectItem value="Grade 12">Grade 12</SelectItem>
                                                </SelectContent>
                                            </Select>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />

                                {/* Extra Curriculars */}
                                <div className="space-y-4">
                                    <div className="flex items-center justify-between">
                                        <div>
                                            <FormLabel>Extra-Curricular Activities</FormLabel>
                                            <FormDescription>
                                                Please list your extra-curricular activities. For each activity, rate your leadership level from 1 to 4 (where 1 is a general Member and 4 is a President/Leader).
                                            </FormDescription>
                                        </div>
                                        <Button
                                            type="button"
                                            variant="outline"
                                            size="sm"
                                            onClick={() => appendExtraCurricular({ name: "", leadership_level: 1 })}
                                            className="gap-2"
                                        >
                                            <Plus className="h-4 w-4" />
                                            Add Activity
                                        </Button>
                                    </div>
                                    {extraCurricularFields.length === 0 && (
                                        <p className="text-sm text-muted-foreground text-center py-4">
                                            No activities added yet. Click "Add Activity" to get started.
                                        </p>
                                    )}
                                    {extraCurricularFields.map((field, index) => (
                                        <div key={field.id} className="flex gap-2 items-start p-4 border rounded-lg">
                                            <div className="flex-1 space-y-4">
                                                <FormField
                                                    control={form.control}
                                                    name={`extra_curriculars.${index}.name`}
                                                    render={({ field }) => (
                                                        <FormItem>
                                                            <FormLabel>Activity Name</FormLabel>
                                                            <FormControl>
                                                                <Input placeholder="e.g., Student Council" {...field} />
                                                            </FormControl>
                                                            <FormMessage />
                                                        </FormItem>
                                                    )}
                                                />
                                                <FormField
                                                    control={form.control}
                                                    name={`extra_curriculars.${index}.leadership_level`}
                                                    render={({ field }) => (
                                                        <FormItem>
                                                            <FormLabel>Leadership Level</FormLabel>
                                                            <Select
                                                                onValueChange={(value) => field.onChange(parseInt(value))}
                                                                value={field.value?.toString()}
                                                            >
                                                                <FormControl>
                                                                    <SelectTrigger>
                                                                        <SelectValue placeholder="Select level" />
                                                                    </SelectTrigger>
                                                                </FormControl>
                                                                <SelectContent>
                                                                    <SelectItem value="1">1 - General Member</SelectItem>
                                                                    <SelectItem value="2">2 - Active Member</SelectItem>
                                                                    <SelectItem value="3">3 - Officer/Coordinator</SelectItem>
                                                                    <SelectItem value="4">4 - President/Leader</SelectItem>
                                                                </SelectContent>
                                                            </Select>
                                                            <FormMessage />
                                                        </FormItem>
                                                    )}
                                                />
                                            </div>
                                            <Button
                                                type="button"
                                                variant="ghost"
                                                size="sm"
                                                onClick={() => removeExtraCurricular(index)}
                                                className="mt-8"
                                            >
                                                <Trash2 className="h-4 w-4 text-destructive" />
                                            </Button>
                                        </div>
                                    ))}
                                </div>

                                {/* Interests */}
                                <FormField
                                    control={form.control}
                                    name="interests"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>What are your major academic or career interests?</FormLabel>
                                            <FormControl>
                                                <MultiSelect
                                                    options={interestOptions}
                                                    selected={field.value}
                                                    onChange={field.onChange}
                                                    placeholder="Select interests..."
                                                    emptyMessage="No interests found."
                                                />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />

                                {/* Courses Taken */}
                                <div className="space-y-4">
                                    <div className="flex items-center justify-between">
                                        <div>
                                            <FormLabel>Which courses have you completed so far?</FormLabel>
                                            <FormDescription>
                                                Add each course you've completed along with your grade (0-100).
                                            </FormDescription>
                                        </div>
                                        <Button
                                            type="button"
                                            variant="outline"
                                            size="sm"
                                            onClick={() => appendCourse({ course: "", grade: 0 })}
                                            className="gap-2"
                                        >
                                            <Plus className="h-4 w-4" />
                                            Add Course
                                        </Button>
                                    </div>
                                    {courseFields.length === 0 && (
                                        <p className="text-sm text-muted-foreground text-center py-4">
                                            No courses added yet. Click "Add Course" to get started.
                                        </p>
                                    )}
                                    {courseFields.map((field, index) => (
                                        <div key={field.id} className="flex gap-2 items-start p-4 border rounded-lg">
                                            <div className="flex-1 space-y-4">
                                                <FormField
                                                    control={form.control}
                                                    name={`courses_taken.${index}.course`}
                                                    render={({ field }) => (
                                                        <FormItem>
                                                            <FormLabel>Course</FormLabel>
                                                            <Select onValueChange={field.onChange} value={field.value}>
                                                                <FormControl>
                                                                    <SelectTrigger>
                                                                        <SelectValue placeholder="Select a course" />
                                                                    </SelectTrigger>
                                                                </FormControl>
                                                                <SelectContent>
                                                                    {courseOptions.map((option) => (
                                                                        <SelectItem key={option.value} value={option.value}>
                                                                            {option.label}
                                                                        </SelectItem>
                                                                    ))}
                                                                </SelectContent>
                                                            </Select>
                                                            <FormMessage />
                                                        </FormItem>
                                                    )}
                                                />
                                                <FormField
                                                    control={form.control}
                                                    name={`courses_taken.${index}.grade`}
                                                    render={({ field }) => (
                                                        <FormItem>
                                                            <FormLabel>Grade (%)</FormLabel>
                                                            <FormControl>
                                                                <Input
                                                                    type="number"
                                                                    placeholder="Enter grade (0-100)"
                                                                    min="0"
                                                                    max="100"
                                                                    {...field}
                                                                    onChange={(e) => field.onChange(parseFloat(e.target.value) || 0)}
                                                                    value={field.value || ""}
                                                                />
                                                            </FormControl>
                                                            <FormMessage />
                                                        </FormItem>
                                                    )}
                                                />
                                            </div>
                                            <Button
                                                type="button"
                                                variant="ghost"
                                                size="sm"
                                                onClick={() => removeCourse(index)}
                                                className="mt-8"
                                            >
                                                <Trash2 className="h-4 w-4 text-destructive" />
                                            </Button>
                                        </div>
                                    ))}
                                </div>

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
