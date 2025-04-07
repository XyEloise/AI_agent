# from langchain_community.llms import GPT4All

# # Instantiate the model. Callbacks support token-wise streaming
# model = GPT4All(model="./models/mistral-7b-openorca.Q4_0.gguf", n_threads=8)

# # Generate text
# response = model.invoke("Once upon a time, ")
from gpt4all import GPT4All
import sys,os

# Suppress error messages during model loading
def suppress_console_output():
    """Temporarily suppress stdout and stderr."""
    sys.stdout.flush()
    sys.stderr.flush()

    # Save original file descriptors
    stdout_fd = os.dup(1)
    stderr_fd = os.dup(2)

    # Open devnull and redirect stdout and stderr
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, 1)
    os.dup2(devnull, 2)
    os.close(devnull)

    return stdout_fd, stderr_fd  # Return saved descriptors

def restore_console_output(stdout_fd, stderr_fd):
    """Restore original stdout and stderr."""
    sys.stdout.flush()
    sys.stderr.flush()
    os.dup2(stdout_fd, 1)
    os.dup2(stderr_fd, 2)
    os.close(stdout_fd)
    os.close(stderr_fd)

# Suppress output only during model loading
stdout_fd, stderr_fd = suppress_console_output()
def load_model():
    try:
        # Define default model, use device="cpu" otherwise it displays an error message when running on a system without a GPU.
        model = GPT4All(r"Zendalona\\LLM\\Llama-3.2-1B-Instruct-Q4_0.gguf",
                        device="cpu", allow_download=False, n_threads=12)
        return model
    finally:
        restore_console_output(stdout_fd, stderr_fd)  # Ensure normal output is restored

if __name__ == '__main__':
    model = load_model()
    response = model.generate("The capital of France is", max_tokens=3)
    print(response)
# def load_model():
#     model = GPT4All(r"D:\shuaibaole\\Intern\\2025\\GPSC 2025\Zendalona\\LLM\\Meta-Llama-3-8B-Instruct.Q4_0.gguf",
#                         device="cpu", allow_download=False)
#     return model

# from gpt4all import GPT4All
