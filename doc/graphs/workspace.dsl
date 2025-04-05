workspace "ChatBot" "Talking with LLM - Simplified Architecture" {

    !identifiers hierarchical

    model {
        u = person "User" "A client uses chatbot for LLM interaction."

        ss = softwareSystem "Chat System" "Allow users to manage conversations, view history, and interact with the LLM API." {
            
            wa = container "Web/Mobile Application" "The frontend interface that allows users to interact with the chat system, sending and receiving messages in real-time." {
                tags "Web/Mobile"
            }

            api = container "API Gateway" "Handles requests from the Web/Mobile application, enforcing authentication, rate-limiting, and routing requests to backend services." {
                tags "Service"
            }

            db = container "Database" "A storage system that maintains chat history, user profiles, session data, and related metadata for persistence and retrieval." {
                tags "Database"
            }

            cache = container "Cache" "A high-speed storage layer that temporarily holds frequently accessed data, reducing latency and improving system performance." {
                tags "Cache"
            }
        }

        cs = softwareSystem "Chat Service" "The backend system responsible for managing active chat sessions, processing messages, routing data, and enforcing business rules." {
            tags "Service"
        }

        lis = softwareSystem "LLM Integration Service" "Handles communication with the LLM API, formatting messages and processing responses." {
            tags "Service"
        }

        ns = softwareSystem "Notification System" "Sends real-time and scheduled notifications to users." {
            tags "Notification"
        }

        llm = softwareSystem "LLM API" "An external AI-powered service that processes natural language inputs and generates responses." {
            tags "External System"
        }

        // User interactions
        u -> ss.wa "Accesses the chat interface"

        // API interactions
        ss.wa -> ss.api "Sends user messages and retrieves responses"
        ss.api -> cs "Routes chat requests"

        // Chat processing flow
        cs -> lis "Sends messages for LLM processing"
        lis -> llm "Forwards requests and processes responses"
        llm -> lis "Returns AI-generated responses"
        lis -> cs "Returns processed responses"

        // Data interactions
        cs -> ss.db "Stores and retrieves chat history"
        ss.api -> ss.db "Loads session data"
        cs -> ss.cache "Uses cache for frequent data"

        // Notifications
        cs -> ns "Triggers notifications"
        ns -> u "Delivers notifications"
    }

    views {
        systemContext ss "System_Context_Diagram" {
            include u ss cs lis ns llm
            autolayout tb
        }

        container ss "Container_Diagram" {
            include *
            autolayout tb
        }

        styles {
            element "Element" {
                color white
            }
            element "Person" {
                background #1E3A5F
                shape person
            }
            element "Software System" {
                background #357ABD
            }
            element "Container" {
                background #357ABD
                shape roundedbox
            }
            element "Database" {
                background #4F4F4F
                shape cylinder
            }
            element "External System" {
                background #0099CC
                shape hexagon
            }
            element "Cache" {
                background #4F4F4F
                shape hexagon
            }
            element "Notification" {
                background #FF4500
            }
            element "Service" {
                background #5F9EA0
            }

            
        }
    }
}