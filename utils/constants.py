# PyBuddy Constants and Datasets

PYTHON_TOPICS = [
    "Variables & Data Types",
    "Control Flow & Loops",
    "Functions & *args/**kwargs",
    "List Comprehensions & Lambdas",
    "Dictionary & Set Comprehensions",
    "Object-Oriented Programming (OOP) Basics",
    "Classes, Inheritance & Polymorphism",
    "Decorators & Closures",
    "Generators & Yield Statements",
    "File Handling & Context Managers (with)",
    "Exception Handling (try-except-finally)",
    "Recursion & Backtracking",
    "Asynchronous Programming (async/await)",
    "Regular Expressions (re module)",
    "Working with Databases (sqlite3)",
    "Testing with unittest/pytest"
]

DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]

# Mini Python Dictionary
PYTHON_DICTIONARY = {
    "lambda": "An anonymous, in-line function defined with the lambda keyword. Usually restricted to a single expression.",
    "yield": "A keyword used in a function like return, but instead of returning a value and ending, it yields a value and pauses execution, returning a generator.",
    "decorator": "A design pattern that allows extending the behavior of an existing function or class without modifying its structure.",
    "generator": "An iterator created by a function containing yield statements. Evaluates values lazily, saving memory.",
    "docstring": "A string literal written as the first statement in a module, function, class, or method definition, used to document the code.",
    "pep 8": "Python Enhancement Proposal 8, the style guide for Python code formatting and standards.",
    "pip": "The package installer for Python, used to download and manage third-party libraries from PyPI.",
    "venv": "A built-in module to create lightweight, isolated virtual environments, preventing dependency conflicts.",
    "mutable": "An object whose state or contents can be changed after creation (e.g., lists, dictionaries, sets).",
    "immutable": "An object whose state or contents cannot be changed after creation (e.g., strings, tuples, integers, frozensets).",
    "list comprehension": "A concise way to create lists using a single line of code, replacing traditional for-loops.",
    "context manager": "An object that defines the runtime context to be established when executing a 'with' statement (e.g., open() for files).",
    "namespace": "A system that has a unique name for each and every object in Python, mapping names to objects to avoid collisions.",
    "dunder methods": "Double-underscore methods (like __init__ or __str__), also called magic methods, which let you define custom behavior for built-in operations.",
    "asyncio": "A Python library to write concurrent code using the async/await syntax, ideal for I/O-bound tasks.",
    "recursion": "A programming technique where a function calls itself directly or indirectly to solve a problem by breaking it down.",
    "serialization": "The process of converting a Python object structure into a byte stream (e.g., using pickle or json) for saving or transmission.",
    "polymorphism": "The ability in OOP to present the same interface for differing underlying data types or classes.",
    "encapsulation": "The OOP concept of wrapping data (variables) and code (methods) together as a single unit, restricting direct access.",
    "garbage collection": "Python's automated memory management system that deletes objects when their reference counts drop to zero."
}

# Tips of the Day
TIPS_OF_THE_DAY = [
    "Tip: Use list comprehensions instead of map() and filter() for cleaner, more readable code.",
    "Tip: Need to merge two dictionaries? In Python 3.9+, you can use the union operator: `dict_a | dict_b`.",
    "Tip: Use `enumerate(iterable)` to get both the index and value of items while looping.",
    "Tip: Use `zip()` to iterate over multiple lists in parallel.",
    "Tip: Utilize the `collections.defaultdict` to avoid KeyError when working with missing dictionary keys.",
    "Tip: Always use virtual environments (`venv`) for your projects to keep dependencies isolated.",
    "Tip: The `with` statement guarantees that system resources (like files) are properly cleaned up after use.",
    "Tip: Use `any()` or `all()` to quickly check boolean conditions across an iterable.",
    "Tip: Use `f-strings` (e.g., `f'{value:.2f}'`) for clean, fast, readable string formatting.",
    "Tip: Use the `get()` method on dictionaries to provide default values if a key doesn't exist."
]

# Random Python Facts
PYTHON_FACTS = [
    "Fact: Python was created by Guido van Rossum and was first released in 1991.",
    "Fact: Python is named after the British comedy troupe 'Monty Python's Flying Circus', not the snake!",
    "Fact: In Python, functions are first-class objects. They can be passed as arguments, returned from functions, and assigned to variables.",
    "Fact: Python does not have a native compiler. It is interpreted and compiled to bytecode (.pyc files) at runtime.",
    "Fact: Zen of Python, a collection of 19 software design principles, is built right into Python. Type `import this` in your terminal to read it!",
    "Fact: The Dutch creator, Guido van Rossum, was given the title 'Benevolent Dictator for Life' (BDFL) until he stepped down in 2018.",
    "Fact: Python has influenced many languages including Go, CoffeeScript, Swift, and Julia.",
    "Fact: In Python, you can chain comparison operators, like `3 < x < 10`.",
    "Fact: Python's lists are implemented as dynamic arrays under the hood, whereas tuples are fixed-size arrays."
]

# Daily Coding Challenges
DAILY_CHALLENGES = [
    {
        "id": 1,
        "title": "Reverse a String",
        "description": "Write a function `reverse_string(s: str) -> str` that returns the string in reverse. Try to do it using Python slicing in a single line.",
        "starter_code": "def reverse_string(s: str) -> str:\n    # Write your code here\n    pass",
        "solution": "def reverse_string(s: str) -> str:\n    return s[::-1]",
        "hint": "Python sequences support slicing. The syntax is [start:stop:step]. A step of -1 goes backwards!"
    },
    {
        "id": 2,
        "title": "FizzBuzz",
        "description": "Write a function `fizzbuzz(n: int) -> list` that returns a list of strings from 1 to n. For multiples of 3 return 'Fizz', for multiples of 5 return 'Buzz', and for multiples of both return 'FizzBuzz'.",
        "starter_code": "def fizzbuzz(n: int) -> list:\n    # Write your code here\n    pass",
        "solution": "def fizzbuzz(n: int) -> list:\n    result = []\n    for i in range(1, n + 1):\n        if i % 3 == 0 and i % 5 == 0:\n            result.append('Fizz`Buzz')\n        elif i % 3 == 0:\n            result.append('Fizz')\n        elif i % 5 == 0:\n            result.append('Buzz')\n        else:\n            result.append(str(i))\n    return result",
        "hint": "Remember to check for divisibility of both 3 and 5 first, otherwise it might fall into 'Fizz' or 'Buzz' prematurely."
    },
    {
        "id": 3,
        "title": "Count Vowels",
        "description": "Write a function `count_vowels(s: str) -> int` that returns the number of vowels ('a', 'e', 'i', 'o', 'u', case-insensitive) in the given string.",
        "starter_code": "def count_vowels(s: str) -> int:\n    # Write your code here\n    pass",
        "solution": "def count_vowels(s: str) -> int:\n    return sum(1 for char in s.lower() if char in 'aeiou')",
        "hint": "Convert the string to lowercase first, then iterate and check if each character is in the vowel string 'aeiou'."
    }
]

# Flashcards
FLASHCARDS = [
    {
        "id": 1,
        "term": "List vs. Tuple",
        "definition": "Lists are mutable (can be changed) and defined with brackets `[1, 2]`. Tuples are immutable (cannot be changed) and defined with parentheses `(1, 2)`. Tuples are generally faster and memory-efficient.",
        "category": "Data Structures"
    },
    {
        "id": 2,
        "term": "Global Interpreter Lock (GIL)",
        "definition": "A mutex that protects access to Python objects, preventing multiple threads from executing Python bytecodes at once in the CPython implementation. This makes standard multi-threading ineffective for CPU-bound tasks.",
        "category": "Concurrency"
    },
    {
        "id": 3,
        "term": "args and kwargs",
        "definition": "`*args` allows a function to accept any number of positional arguments as a tuple. `**kwargs` allows accepting any number of keyword arguments as a dictionary.",
        "category": "Functions"
    },
    {
        "id": 4,
        "term": "List Comprehension",
        "definition": "A compact syntactic way to create a list from an iterable. Example: `[x**2 for x in range(10) if x % 2 == 0]` creates a list of squares for even numbers.",
        "category": "Syntax"
    },
    {
        "id": 5,
        "term": "Decorators",
        "definition": "Functions that wrap another function to modify or extend its behavior without changing its code. They use the `@decorator_name` syntax.",
        "category": "Advanced Python"
    }
]

# Interview Questions
INTERVIEW_QUESTIONS = {
    "Junior": [
        {
            "question": "What is Python and why is it so popular?",
            "answer": "Python is an interpreted, high-level, general-purpose programming language. It is popular because of its simple, readable syntax (like English), massive ecosystem of libraries (for web, AI, data science), active community, and versatility across platforms."
        },
        {
            "question": "Explain the difference between 'is' and '==' operators.",
            "answer": "'==' compares the values of two objects (equality). 'is' compares the memory addresses (identities) of two objects, checking if they refer to the exact same object in memory."
        },
        {
            "question": "What are local and global variables?",
            "answer": "A local variable is declared inside a function and can only be accessed within that function. A global variable is declared outside functions and is accessible throughout the entire script. You use the `global` keyword inside a function to modify a global variable."
        }
    ],
    "Mid": [
        {
            "question": "How does memory management work in Python?",
            "answer": "Python manages memory dynamically through a private heap. It uses reference counting to track active objects and a cyclic garbage collector to destroy objects that reference each other but are no longer reachable from the code."
        },
        {
            "question": "What is the difference between deep copy and shallow copy?",
            "answer": "A shallow copy (`copy.copy()`) creates a new collection object but populates it with references to the child objects. A deep copy (`copy.deepcopy()`) recursively copies everything, meaning the new collection has its own independent copies of all child objects."
        },
        {
            "question": "What are generators, and how do they save memory?",
            "answer": "Generators are functions that return an iterator using the `yield` keyword. Instead of building the entire dataset in memory and returning it as a list, they generate one item at a time on the fly (lazy evaluation), which is highly memory-efficient for large files or streams."
        }
    ],
    "Senior": [
        {
            "question": "What is the GIL (Global Interpreter Lock) and how do you bypass it?",
            "answer": "The GIL is a mechanism in CPython that ensures only one thread executes Python bytecode at any given time, protecting internal memory from race conditions. To bypass the GIL for CPU-bound tasks, you can use the `multiprocessing` module (which spawns separate OS processes, each with its own interpreter and memory space) or run performance-critical code in C/C++ extensions or tools like Cython/Numba."
        },
        {
            "question": "Explain Python's Method Resolution Order (MRO).",
            "answer": "MRO is the order in which Python searches for a method or attribute in a class hierarchy under multiple inheritance. Python 3 uses the C3 Linearization algorithm to determine a deterministic search order, which can be viewed for any class via `MyClass.__mro__` or `MyClass.mro()`."
        },
        {
            "question": "What are metaclasses and when would you use them?",
            "answer": "A metaclass is the class of a class. While classes define how instances behave, metaclasses define how classes themselves behave (classes are instances of metaclasses, usually `type`). They are used to intercept class creation, validate class structures at definition time, automatically register classes in registry patterns, or inject attributes dynamically (often used in ORMs like Django models)."
        }
    ]
}

# Study Plan Template Roadmap
CODING_ROADMAP = [
    {
        "phase": "Level 1: Python Basics",
        "description": "Master variables, data types, standard operators, and basic input/output operations.",
        "milestones": ["Understand dynamic typing", "Use strings, integers, floats, booleans", "Perform basic user input with input()"]
    },
    {
        "phase": "Level 2: Control Flow & Structures",
        "description": "Control execution using conditional statements and repeat blocks with loops.",
        "milestones": ["If-elif-else statements", "For and while loops", "List, Tuple, and Dictionary basics"]
    },
    {
        "phase": "Level 3: Functional Programming",
        "description": "Structure code into reusable units (functions) and apply functional constructs.",
        "milestones": ["Function definitions and return values", "*args and **kwargs parameter packing", "Lambda functions and list comprehensions"]
    },
    {
        "phase": "Level 4: Intermediate Python Concepts",
        "description": "Learn clean resource management and robust error handling frameworks.",
        "milestones": ["Try-except-finally exceptions", "With context managers for files", "Creating custom generator functions with yield"]
    },
    {
        "phase": "Level 5: OOP & Advanced Paradigms",
        "description": "Design modular projects using object orientation, decorators, and concurrency.",
        "milestones": ["Classes, inheritance, and dunder methods", "Creating custom decorators", "Asynchronous async/await functions"]
    }
]
