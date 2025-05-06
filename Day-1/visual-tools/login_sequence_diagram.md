```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant Database

    User->>Frontend: Enters username and password
    Frontend->>Backend: Sends login request (username, password)
    Backend->>Database: Authenticates user credentials
    Database-->>Backend: Authentication result (success/failure)
    alt Authentication successful
        Backend->>Frontend: Authentication success
        Frontend->>User: Login successful, redirects to dashboard
        Frontend->>Backend: Retrieves user session
        Backend->>Database: Fetches user data
        Database-->>Backend: User data
        Backend-->>Frontend: User data
        Frontend->>User: Displays dashboard
    else Authentication failed
        Backend->>Frontend: Authentication failure
        Frontend->>User: Displays login error message
    end