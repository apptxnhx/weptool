# Replit.md

## Overview

This is a full-stack weapon statistics web application for the game TACTICOOL. The application displays comprehensive weapon information including stats, categories, and detailed specifications. It's built as a modern web application with a React frontend and Express backend, featuring a clean and responsive design with gaming aesthetics.

## System Architecture

The application follows a monolithic full-stack architecture with clear separation between client and server code:

- **Frontend**: React-based single-page application with TypeScript
- **Backend**: Express.js server with RESTful API endpoints
- **Database**: PostgreSQL with Drizzle ORM for type-safe database operations
- **Build System**: Vite for frontend bundling and development
- **Styling**: Tailwind CSS with shadcn/ui component library
- **Deployment**: Configured for Replit with autoscale deployment

## Key Components

### Frontend Architecture
- **Framework**: React 18 with TypeScript
- **Routing**: Wouter for lightweight client-side routing
- **State Management**: TanStack Query for server state management
- **UI Components**: shadcn/ui component library built on Radix UI primitives
- **Styling**: Tailwind CSS with custom TACTICOOL theme colors
- **Form Handling**: React Hook Form with Zod validation

### Backend Architecture
- **Server**: Express.js with TypeScript
- **Database ORM**: Drizzle ORM with PostgreSQL dialect
- **Database Provider**: Neon Database (@neondatabase/serverless)
- **Session Storage**: PostgreSQL session store (connect-pg-simple)
- **Development**: Hot reload with tsx and Vite middleware integration

### Database Schema
The application uses two main tables:
- **weapons**: Stores weapon information including name, category, rarity, stats, and images
- **users**: User authentication with username/password (prepared for future features)

Key schema decisions:
- JSON field for flexible weapon stats storage
- Serial primary keys for simple relationships
- Text fields for categorical data (category, rarity, primary weapon type)

## Data Flow

1. **Client Request**: User navigates to weapon categories or searches for weapons
2. **API Layer**: Express routes handle requests (`/api/weapons/:category`, `/api/categories`, `/api/weapons/:category/search`)
3. **Storage Layer**: Memory storage implementation provides weapon data (currently using static data, designed to be replaced with database queries)
4. **Response**: JSON data returned to client
5. **UI Update**: React Query manages cache and UI updates

The application currently uses in-memory storage with static weapon data, but the architecture supports easy migration to database-backed storage.

## External Dependencies

### Core Dependencies
- **@neondatabase/serverless**: PostgreSQL database connectivity
- **drizzle-orm**: Type-safe ORM with automatic migrations
- **@tanstack/react-query**: Server state management and caching
- **express**: Web server framework
- **react**: Frontend framework
- **vite**: Build tool and development server

### UI Dependencies
- **@radix-ui/***: Accessible UI primitives
- **tailwindcss**: Utility-first CSS framework
- **lucide-react**: Icon library
- **class-variance-authority**: Utility for creating variant-based component APIs

### Development Dependencies
- **typescript**: Type safety across the stack
- **tsx**: TypeScript execution for development
- **esbuild**: Fast bundling for production server builds

## Deployment Strategy

The application is configured for Replit deployment with the following approach:

1. **Development**: `npm run dev` starts both frontend and backend in development mode
2. **Build Process**: 
   - Frontend: Vite builds React application to `dist/public`
   - Backend: esbuild bundles server code to `dist/index.js`
3. **Production**: `npm run start` runs the production server
4. **Database**: PostgreSQL module configured in Replit environment
5. **Auto-scaling**: Configured for autoscale deployment target

The server serves static files in production and integrates Vite middleware in development for hot reloading.

## User Preferences

Preferred communication style: Simple, everyday language.

## Changelog

Changelog:
- June 20, 2025. Initial setup