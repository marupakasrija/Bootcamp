from collections import deque

# Simulate a Stack (LIFO - Last In, First Out)
# Use append() to push and pop() to pop
stack = deque()
print("Simulating Stack:")
stack.append(10)
print(f"Pushed 10: {list(stack)}")
stack.append(20)
print(f"Pushed 20: {list(stack)}")
stack.append(30)
print(f"Pushed 30: {list(stack)}")

print(f"Popped: {stack.pop()}") # Output: 30
print(f"Stack now: {list(stack)}")
print(f"Popped: {stack.pop()}") # Output: 20
print(f"Stack now: {list(stack)}")

# Simulate a Queue (FIFO - First In, First Out)
# Use append() to enqueue and popleft() to dequeue
queue = deque()
print("\nSimulating Queue:")
queue.append(100)
print(f"Enqueued 100: {list(queue)}")
queue.append(200)
print(f"Enqueued 200: {list(queue)}")
queue.append(300)
print(f"Enqueued 300: {list(queue)}")

print(f"Dequeued: {queue.popleft()}") # Output: 100
print(f"Queue now: {list(queue)}")
print(f"Dequeued: {queue.popleft()}") # Output: 200
print(f"Queue now: {list(queue)}")