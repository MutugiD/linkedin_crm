# Development Prompts for LinkedIn CRM Automation

This document contains prompts and questions to guide the development process at each stage.

## Project Setup Phase

1. What are the minimum Python requirements for this project?
2. What database structure would be optimal for storing LinkedIn data?
3. What authentication method would be most secure yet user-friendly?
4. How should we handle environment variables and secrets?
5. What Docker configuration will provide the best development experience?

## LinkedIn Scraping Phase

1. What techniques can be used to scrape LinkedIn without cookies?
2. How can we avoid rate limiting and detection?
3. What data points are most valuable to extract from:
   - LinkedIn profiles?
   - Company pages?
   - Posts and content?
4. How should we structure the scraped data?
5. What proxy rotation strategy should we implement?
6. How can we ensure data quality and handle missing information?

## Lead Scoring Phase

1. What factors define an Ideal Customer Profile (ICP)?
2. How should we weight different criteria (industry, role, revenue, etc.)?
3. What algorithms would provide the most accurate scoring?
4. How can we dynamically update scores based on new information?
5. What thresholds should trigger automated actions?

## Outreach Automation Phase

1. What message templates would be most effective for different stages?
2. How should we schedule outreach to avoid detection?
3. What sentiment analysis techniques would best identify response sentiment?
4. How should we determine when conversations have gone cold?
5. What follow-up strategies would be most effective?

## Pipeline Management Phase

1. What pipeline stages should we define?
2. What triggers should move leads between stages?
3. How can we integrate sentiment analysis into pipeline management?
4. What metrics should we track for pipeline performance?
5. How should we handle pipeline stage visualization?

## Frontend Development Phase

1. What dashboard metrics are most important for users?
2. How should we design the lead management interface for optimal usability?
3. What team management features are essential?
4. How should we implement real-time notifications?
5. What customization options should be available to users?

## Testing Phase

1. What are the critical paths that need thorough testing?
2. How can we simulate LinkedIn's behavior for testing?
3. What performance metrics should we target?
4. How can we test the system at scale?
5. What security tests should we prioritize?

## Deployment Phase

1. What cloud infrastructure would be most cost-effective?
2. How should we handle database backups and migrations?
3. What monitoring tools should we implement?
4. How should we structure the CI/CD pipeline?
5. What disaster recovery procedures should be in place?

## Feature-Specific Prompts

### Key Players Finder

1. What criteria define a "key player" in a company?
2. How can we extract seniority and influence from LinkedIn profiles?
3. What data visualization would best present key players?

### Custom LinkedIn Search Exports

1. What search parameters are most valuable for users?
2. How can we structure export formats for different needs?
3. What filtering options should be available post-search?

### Company News Finder

1. What sources beyond LinkedIn should we monitor for company news?
2. How can we determine news relevance?
3. How should we present and categorize news items?

## Integration Prompts

1. What APIs might users want to connect with this system?
2. How can we ensure data consistency across integrations?
3. What webhook events should we expose?
4. How should we handle authentication for third-party services?
5. What data export formats should we support?