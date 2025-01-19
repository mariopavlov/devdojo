import ast
import sys
import unittest
import io
from typing import Dict, Any, Tuple
from dataclasses import dataclass
import traceback

@dataclass
class RunResult:
    success: bool
    output: str
    error_message: str = ""

class CodeRunner:
    @staticmethod
    def validate_syntax(code: str) -> RunResult:
        """Validate Python code syntax without executing it."""
        try:
            ast.parse(code)
            return RunResult(success=True, output="Code syntax is valid")
        except SyntaxError as e:
            return RunResult(
                success=False,
                output="",
                error_message=f"Syntax Error: {str(e)}"
            )
        except Exception as e:
            return RunResult(
                success=False,
                output="",
                error_message=f"Validation Error: {str(e)}"
            )

    @staticmethod
    def run_tests(source_code: str, test_code: str) -> RunResult:
        """Run unit tests against the provided source code."""
        # Create a new test loader and runner
        loader = unittest.TestLoader()
        runner = unittest.TextTestRunner(stream=io.StringIO())

        try:
            # Execute source code in a new namespace
            namespace = {}
            exec(source_code, namespace)
            
            # Execute test code in the same namespace
            exec(test_code, namespace)
            
            # Find and run tests
            test_cases = [
                obj for name, obj in namespace.items()
                if isinstance(obj, type) and issubclass(obj, unittest.TestCase)
            ]
            
            if not test_cases:
                return RunResult(
                    success=False,
                    output="",
                    error_message="No test cases found"
                )

            suite = unittest.TestSuite()
            for test_case in test_cases:
                suite.addTests(loader.loadTestsFromTestCase(test_case))

            # Run tests and capture output
            stream = io.StringIO()
            runner = unittest.TextTestRunner(stream=stream)
            result = runner.run(suite)
            
            success = result.wasSuccessful()
            output = stream.getvalue()
            
            return RunResult(
                success=success,
                output=output,
                error_message="" if success else "Some tests failed"
            )

        except Exception as e:
            return RunResult(
                success=False,
                output="",
                error_message=f"Test Execution Error: {str(e)}\n{traceback.format_exc()}"
            )

    @staticmethod
    def execute_code(code: str) -> RunResult:
        """Execute the provided code and capture its output."""
        # Redirect stdout to capture print statements
        stdout = io.StringIO()
        sys.stdout = stdout
        
        try:
            exec(code)
            output = stdout.getvalue()
            return RunResult(success=True, output=output)
        except Exception as e:
            return RunResult(
                success=False,
                output=stdout.getvalue(),
                error_message=f"Execution Error: {str(e)}\n{traceback.format_exc()}"
            )
        finally:
            sys.stdout = sys.__stdout__
