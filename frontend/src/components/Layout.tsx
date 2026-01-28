import { ReactNode } from 'react';
import { Link } from 'react-router-dom';

interface LayoutProps {
    children: ReactNode;
}

const Header = () => (
    <header className="bg-background shadow-sm border-b">
        <div className="container mx-auto px-4 py-4">
            <Link to="/" className="text-xl font-bold">AdmitTree</Link>
            {/* Add navigation, logo, etc. */}
        </div>
    </header>
);

const Footer = () => (
    <footer className="bg-background border-t mt-auto">
        <div className="container mx-auto px-4 py-6 text-center text-sm text-muted-foreground">
            © 2026 AdmitTree. All rights reserved.
        </div>
    </footer>
);

export const Layout = ({ children }: LayoutProps) => (
    <div className="min-h-screen flex flex-col">
        <Header />
        <main className="flex-1">{children}</main>
        <Footer />
    </div>
);
