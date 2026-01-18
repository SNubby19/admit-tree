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
import { Switch } from "@/components/ui/switch";
import { ArrowLeft, ArrowRight, Loader2, Plus, Trash2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { UniversityProgram } from "@/types/application";
import { ProgramSelectionModal } from "@/components/ProgramSelectionModal";

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
    wants_coop: z.boolean().default(false),
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
    { value: "MTH1W", label: "MTH1W - De-streamed Math" },
    { value: "ENL1W", label: "ENL1W - De-streamed English" },
    { value: "SNC1W", label: "SNC1W - De-streamed Science" },
    { value: "TAS1O", label: "TAS1O - Technology and the Skilled Trades" },
    { value: "MPM2D", label: "MPM2D - Principles of Mathematics (Academic)" },
    { value: "ENG2D", label: "ENG2D - English (Academic)" },
    { value: "SNC2D", label: "SNC2D - Science (Academic)" },
    { value: "TAS2O", label: "TAS2O - Technology and the Skilled Trades" },
    { value: "MCR3U", label: "MCR3U - Functions" },
    { value: "NBE3U", label: "NBE3U - Contemporary Indigenous Voices" },
    { value: "SCH3U", label: "SCH3U - Chemistry" },
    { value: "SPH3U", label: "SPH3U - Physics" },
    { value: "ICS3U", label: "ICS3U - Intro to Computer Science" },
    { value: "TEJ3M", label: "TEJ3M - Computer Engineering Technology" },
    { value: "TGJ3M", label: "TGJ3M - Communications Technology" },
    { value: "MHF4U", label: "MHF4U - Advanced Functions" },
    { value: "MCV4U", label: "MCV4U - Calculus and Vectors" },
    { value: "ENG4U", label: "ENG4U - English" },
    { value: "SCH4U", label: "SCH4U - Chemistry" },
    { value: "SPH4U", label: "SPH4U - Physics" },
    { value: "ICS4U", label: "ICS4U - Computer Science" },
    { value: "MDM4U", label: "MDM4U - Mathematics of Data Management" },
    { value: "TEJ4M", label: "TEJ4M - Computer Engineering Technology" },
    { value: "TGJ4M", label: "TGJ4M - Communications Technology" },
];

interface ProgramRanking {
    university: string;
    program: string;
    score: number;
    breakdown: {
        academic: number;
        interest: number;
        ec: number;
        coop_fit: number;
    };
}

const Intake = () => {
    const navigate = useNavigate();
    const { toast } = useToast();
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [showSelectionModal, setShowSelectionModal] = useState(false);
    const [programRankings, setProgramRankings] = useState<ProgramRanking[]>([]);
    const [pendingFormData, setPendingFormData] = useState<IntakeFormData | null>(null);

    const form = useForm<IntakeFormData>({
        resolver: zodResolver(intakeSchema),
        defaultValues: {
            name: "",
            email: "",
            grade: "",
            wants_coop: false,
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

    const handleProgramSelection = (selectedIndices: number[]) => {
        if (!pendingFormData) return;

        // Transform selected rankings to UniversityProgram format
        const selectedPrograms: UniversityProgram[] = selectedIndices.map((index) => {
            const ranking = programRankings[index];
            return {
                id: `program-${index + 1}`,
                universityName: ranking.university,
                programName: ranking.program,
                deadline: "2025-01-15", // Default deadline, can be enhanced later
                overallProgress: 0, // New programs start at 0%
                steps: [], // Can be populated later
                bonusTasks: [],
            };
        });

        // Store student profile and selected programs
        const roadmapId = `roadmap-${Date.now()}`;
        const studentProfile = {
            name: pendingFormData.name,
            email: pendingFormData.email,
            grade: pendingFormData.grade,
            wants_coop: pendingFormData.wants_coop,
            extra_curriculars: pendingFormData.extra_curriculars,
            interests: pendingFormData.interests,
            courses_taken: pendingFormData.courses_taken,
        };

        const newRoadmap = {
            id: roadmapId,
            student_profile: studentProfile,
            programs: selectedPrograms,
            createdAt: new Date().toISOString(),
        };

        // Store in localStorage
        const existingRoadmaps = JSON.parse(localStorage.getItem("userRoadmaps") || "[]");
        existingRoadmaps.push(newRoadmap);
        localStorage.setItem("userRoadmaps", JSON.stringify(existingRoadmaps));
        localStorage.setItem("currentRoadmap", JSON.stringify(newRoadmap));
        localStorage.setItem("currentPrograms", JSON.stringify(selectedPrograms));

        setShowSelectionModal(false);
        setPendingFormData(null);
        setProgramRankings([]);

        toast({
            title: "Roadmap Created!",
            description: `Added ${selectedPrograms.length} program${selectedPrograms.length !== 1 ? "s" : ""} to your dashboard.`,
        });

        navigate("/dashboard");
    };

    const handleCancelSelection = () => {
        setShowSelectionModal(false);
        setPendingFormData(null);
        setProgramRankings([]);
    };

    const onSubmit = async (data: IntakeFormData) => {
        setIsSubmitting(true);

        try {
            // Calculate average from courses
            const average = data.courses_taken.reduce((sum, course) => sum + course.grade, 0) / data.courses_taken.length;

            // Convert grade string to int (e.g., "Grade 9" -> 9)
            const gradeLevel = parseInt(data.grade.replace("Grade ", ""));

            // Transform data to match backend API format
            const backendPayload = {
                grade_level: gradeLevel,
                average: average,
                wants_coop: data.wants_coop,
                extra_curriculars: data.extra_curriculars.map((ec) => [ec.name, ec.leadership_level]),
                major_interests: data.interests,
                courses_taken: data.courses_taken.map((course) => [course.course, course.grade]),
            };

            // Call backend API
            const response = await fetch("http://localhost:5001/api/recommend", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(backendPayload),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || "Failed to get recommendations");
            }

            const apiResponse = await response.json();

            // Store form data and rankings, then show selection modal
            setPendingFormData(data);
            setProgramRankings(apiResponse.rankings);
            setIsSubmitting(false);
            setShowSelectionModal(true);
        } catch (error) {
            setIsSubmitting(false);
            toast({
                title: "Error",
                description: error instanceof Error ? error.message : "Failed to create roadmap. Please try again.",
                variant: "destructive",
            });
        }
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

                                {/* Co-op Preference */}
                                <FormField
                                    control={form.control}
                                    name="wants_coop"
                                    render={({ field }) => (
                                        <FormItem className="flex flex-row items-center justify-between rounded-lg border p-4">
                                            <div className="space-y-0.5">
                                                <FormLabel className="text-base">Are you interested in co-op programs?</FormLabel>
                                                <FormDescription>
                                                    Co-op programs offer work experience opportunities during your studies
                                                </FormDescription>
                                            </div>
                                            <FormControl>
                                                <Switch
                                                    checked={field.value}
                                                    onCheckedChange={field.onChange}
                                                />
                                            </FormControl>
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

            {/* Program Selection Modal */}
            <ProgramSelectionModal
                open={showSelectionModal}
                rankings={programRankings}
                onConfirm={handleProgramSelection}
                onCancel={handleCancelSelection}
            />
        </div>
    );
};

export default Intake;
