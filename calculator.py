import tkinter as tk
from tkinter import font

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("400x600")
        self.root.configure(bg="#000000")
        self.root.resizable(False, False)
        
        # Display variable
        self.display_var = tk.StringVar(value="0")
        self.current_input = "0"
        self.operator = None
        self.previous_value = None
        self.should_reset_display = False
        
        # Create display
        self.create_display()
        
        # Create buttons
        self.create_buttons()
    
    def create_display(self):
        """Create the display screen"""
        display_frame = tk.Frame(self.root, bg="#000000")
        display_frame.pack(pady=20, padx=20, fill=tk.BOTH)
        
        display_label = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=("Helvetica", 60, "bold"),
            bg="#000000",
            fg="#FFFFFF",
            anchor="e",
            justify="right"
        )
        display_label.pack(fill=tk.BOTH, expand=True)
    
    def create_buttons(self):
        """Create calculator buttons in iOS style"""
        button_frame = tk.Frame(self.root, bg="#000000")
        button_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Button layout (same as iOS calculator)
        buttons = [
            ["AC", "+/-", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "="]
        ]
        
        # Color scheme
        operation_color = "#FF9500"
        number_color = "#333333"
        equals_color = "#FF9500"
        zero_button_color = "#333333"
        
        for row_idx, row in enumerate(buttons):
            row_frame = tk.Frame(button_frame, bg="#000000")
            row_frame.pack(fill=tk.BOTH, expand=True, pady=5)
            
            for col_idx, btn_text in enumerate(row):
                # Determine button color
                if btn_text in ["AC", "+/-", "%"]:
                    btn_color = operation_color
                    text_color = "#000000"
                elif btn_text in ["÷", "×", "-", "+"]:
                    btn_color = operation_color
                    text_color = "#FFFFFF"
                elif btn_text == "=":
                    btn_color = equals_color
                    text_color = "#FFFFFF"
                elif btn_text == "0":
                    btn_color = zero_button_color
                    text_color = "#FFFFFF"
                else:
                    btn_color = number_color
                    text_color = "#FFFFFF"
                
                # Create button
                btn = tk.Button(
                    row_frame,
                    text=btn_text,
                    font=("Helvetica", 20, "bold"),
                    bg=btn_color,
                    fg=text_color,
                    activebackground="#555555",
                    activeforeground="#FFFFFF",
                    bd=0,
                    highlightthickness=0,
                    padx=15,
                    pady=20,
                    command=lambda x=btn_text: self.on_button_click(x)
                )
                
                # Handle 0 button spanning 2 columns
                if btn_text == "0":
                    btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2.5)
                    # Add space for the decimal point to the right
                    spacer = tk.Frame(row_frame, bg="#000000")
                    spacer.pack(side=tk.LEFT, expand=True, padx=2.5)
                else:
                    btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2.5)
    
    def on_button_click(self, btn_text):
        """Handle button clicks"""
        if btn_text == "AC":
            self.clear()
        elif btn_text == "+/-":
            self.toggle_sign()
        elif btn_text in ["÷", "×", "-", "+"]:
            self.set_operator(btn_text)
        elif btn_text == "=":
            self.calculate()
        elif btn_text == "%":
            self.percentage()
        elif btn_text == ".":
            self.add_decimal()
        else:
            self.append_number(btn_text)
    
    def append_number(self, num):
        """Append number to display"""
        if self.should_reset_display:
            self.current_input = num
            self.should_reset_display = False
        else:
            if self.current_input == "0":
                self.current_input = num
            else:
                self.current_input += num
        
        self.display_var.set(self.current_input)
    
    def add_decimal(self):
        """Add decimal point"""
        if self.should_reset_display:
            self.current_input = "0."
            self.should_reset_display = False
        elif "." not in self.current_input:
            self.current_input += "."
        
        self.display_var.set(self.current_input)
    
    def set_operator(self, op):
        """Set operator for calculation"""
        try:
            self.previous_value = float(self.current_input)
            self.operator = op
            self.should_reset_display = True
        except ValueError:
            pass
    
    def calculate(self):
        """Perform calculation"""
        if self.operator is None or self.previous_value is None:
            return
        
        try:
            current = float(self.current_input)
            
            if self.operator == "+":
                result = self.previous_value + current
            elif self.operator == "-":
                result = self.previous_value - current
            elif self.operator == "×":
                result = self.previous_value * current
            elif self.operator == "÷":
                if current != 0:
                    result = self.previous_value / current
                else:
                    self.display_var.set("Error")
                    self.current_input = "0"
                    return
            
            # Format result
            if result == int(result):
                self.current_input = str(int(result))
            else:
                self.current_input = str(round(result, 10))
            
            self.display_var.set(self.current_input)
            self.operator = None
            self.previous_value = None
            self.should_reset_display = True
        except ValueError:
            pass
    
    def clear(self):
        """Clear display"""
        self.current_input = "0"
        self.operator = None
        self.previous_value = None
        self.should_reset_display = False
        self.display_var.set(self.current_input)
    
    def toggle_sign(self):
        """Toggle between positive and negative"""
        try:
            value = float(self.current_input)
            value = -value
            self.current_input = str(int(value) if value == int(value) else value)
            self.display_var.set(self.current_input)
        except ValueError:
            pass
    
    def percentage(self):
        """Convert to percentage"""
        try:
            value = float(self.current_input)
            value = value / 100
            self.current_input = str(value)
            self.display_var.set(self.current_input)
        except ValueError:
            pass


if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
