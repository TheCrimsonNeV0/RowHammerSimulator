# Simplified simulator of the Row Hammer Attack written in Python

University of North Florida
CIS 6372 - Information Assurance

This tool simulates the memory behavior in Python. Each cell holds the access count and the bit flips are probabilistically determined by a function

- Memory behavior implemented
- Multiple accessor threads added to simulate CPU behavior (hammer, display)
- Probabilistically decide if a bit flip occurs considering access count: This step uses the function proposed by Hammulator
- Target Row Refresh implemented
- Probabilistic Adjacent Row Activation implemented
