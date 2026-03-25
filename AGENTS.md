# Project Rules

## Prompt Logging
Every time you receive a new instruction or prompt, append it to prompts.txt in the project root with a timestamp (ISO 8601) and a brief summary of what you did in response. Create the file if it doesn't exist. Keep this log updated throughout all sessions.

## Design Patterns

### KISS (Keep It Simple, Stupid)
- Prefer simple, readable code over clever solutions
- Avoid unnecessary abstraction or complexity
- Solve the problem directly first, then refactor if needed

### SOLID
- **S**ingle Responsibility: Each class/function does one thing well
- **O**pen/Closed: Open for extension, closed for modification
- **L**iskov Substitution: Subtypes must be substitutable for their base types
- **I**nterface Segregation: Prefer small, specific interfaces over large ones
- **D**ependency Inversion: Depend on abstractions, not concrete implementations

### Conventional Commits
Format: `<type>(<scope>): <description>`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding/updating tests
- `chore`: Maintenance

Example: `feat(core): add voting functionality`

### TDD (Test-Driven Development)
1. Write a failing test first
2. Write minimal code to pass the test
3. Refactor while keeping tests passing

### DDD (Domain-Driven Design)
- Focus on the core domain logic
- Use meaningful domain terms in code
- Separate domain logic from infrastructure
- Keep models simple and focused on business rules

