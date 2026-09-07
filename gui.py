"""
Tkinter GUI for RAG Application
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
from rag_engine import RAGEngine


class RAGApplicationGUI:
    """Tkinter GUI for Retrieval-Augmented Generation Application"""
    
    def __init__(self, root):
        """Initialize the GUI"""
        self.root = root
        self.root.title("Tkinter RAG Application with ChromaDB")
        self.root.geometry("1200x800")
        
        # Initialize RAG engine
        self.rag_engine = RAGEngine()
        self.is_processing = False
        
        # Create GUI components
        self._create_widgets()
        self._setup_styles()
    
    def _setup_styles(self):
        """Setup ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
    
    def _create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title = ttk.Label(main_frame, text="RAG Q&A System with ChromaDB", 
                         font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Knowledge Base Frame
        kb_frame = ttk.LabelFrame(main_frame, text="Knowledge Base Management", padding="10")
        kb_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        kb_frame.columnconfigure(1, weight=1)
        
        ttk.Label(kb_frame, text="Document ID:").grid(row=0, column=0, sticky=tk.W)
        self.doc_id_entry = ttk.Entry(kb_frame)
        self.doc_id_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        ttk.Label(kb_frame, text="Document Content:").grid(row=1, column=0, sticky=(tk.W, tk.N), pady=5)
        self.doc_content = scrolledtext.ScrolledText(kb_frame, height=6, width=60)
        self.doc_content.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # Buttons frame
        button_frame = ttk.Frame(kb_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Add Document", 
                  command=self.add_document).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load from File", 
                  command=self.load_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove Document", 
                  command=self.remove_document).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Show Stats", 
                  command=self.show_stats).pack(side=tk.LEFT, padx=5)
        
        # Query Frame
        query_frame = ttk.LabelFrame(main_frame, text="Question & Answer", padding="10")
        query_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        query_frame.columnconfigure(1, weight=1)
        query_frame.rowconfigure(1, weight=1)
        query_frame.rowconfigure(3, weight=1)
        
        ttk.Label(query_frame, text="Your Question:").grid(row=0, column=0, sticky=(tk.W, tk.N))
        self.question_entry = scrolledtext.ScrolledText(query_frame, height=4, width=80)
        self.question_entry.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Ask button
        ttk.Button(query_frame, text="Ask Question", 
                  command=self.ask_question).grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Label(query_frame, text="Answer:").grid(row=3, column=0, sticky=(tk.W, tk.N), pady=(10, 0))
        self.answer_text = scrolledtext.ScrolledText(query_frame, height=10, width=80)
        self.answer_text.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
    
    def add_document(self):
        """Add a document to the knowledge base"""
        doc_id = self.doc_id_entry.get().strip()
        content = self.doc_content.get("1.0", tk.END).strip()
        
        if not doc_id or not content:
            messagebox.showwarning("Input Error", "Please enter both Document ID and Content")
            return
        
        self.status_var.set("Adding document...")
        self.root.update()
        
        # Run in background thread
        thread = threading.Thread(target=self._add_document_thread, args=(doc_id, content))
        thread.start()
    
    def _add_document_thread(self, doc_id, content):
        """Add document in background thread"""
        try:
            result = self.rag_engine.add_knowledge(doc_id, content)
            
            if result['success']:
                messagebox.showinfo("Success", result['message'])
                self.doc_id_entry.delete(0, tk.END)
                self.doc_content.delete("1.0", tk.END)
            else:
                messagebox.showerror("Error", result['message'])
            
            self.status_var.set("Ready")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add document: {str(e)}")
            self.status_var.set("Error")
    
    def load_file(self):
        """Load a document from a text file"""
        file_path = filedialog.askopenfilename(
            title="Select a text file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Use filename as document ID
            import os
            doc_id = os.path.splitext(os.path.basename(file_path))[0]
            
            self.doc_id_entry.delete(0, tk.END)
            self.doc_id_entry.insert(0, doc_id)
            
            self.doc_content.delete("1.0", tk.END)
            self.doc_content.insert("1.0", content)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def remove_document(self):
        """Remove a document from the knowledge base"""
        doc_id = self.doc_id_entry.get().strip()
        
        if not doc_id:
            messagebox.showwarning("Input Error", "Please enter a Document ID")
            return
        
        if messagebox.askyesno("Confirm", f"Remove document '{doc_id}'?"):
            self.status_var.set("Removing document...")
            self.root.update()
            
            thread = threading.Thread(target=self._remove_document_thread, args=(doc_id,))
            thread.start()
    
    def _remove_document_thread(self, doc_id):
        """Remove document in background thread"""
        try:
            result = self.rag_engine.remove_knowledge(doc_id)
            messagebox.showinfo("Success", result['message'])
            self.status_var.set("Ready")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove document: {str(e)}")
            self.status_var.set("Error")
    
    def show_stats(self):
        """Show knowledge base statistics"""
        try:
            stats = self.rag_engine.get_stats()
            message = f"Total Chunks: {stats['total_chunks']}\n\nDocuments:\n" + \
                     "\n".join(stats['documents'][:10])  # Show first 10
            messagebox.showinfo("Knowledge Base Statistics", message)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get stats: {str(e)}")
    
    def ask_question(self):
        """Ask a question to the RAG system"""
        question = self.question_entry.get("1.0", tk.END).strip()
        
        if not question:
            messagebox.showwarning("Input Error", "Please enter a question")
            return
        
        self.status_var.set("Processing question...")
        self.answer_text.config(state=tk.NORMAL)
        self.answer_text.delete("1.0", tk.END)
        self.answer_text.insert("1.0", "Generating answer...")
        self.root.update()
        
        # Run in background thread
        thread = threading.Thread(target=self._ask_question_thread, args=(question,))
        thread.start()
    
    def _ask_question_thread(self, question):
        """Ask question in background thread"""
        try:
            result = self.rag_engine.generate_answer(question)
            
            # Display answer
            self.answer_text.config(state=tk.NORMAL)
            self.answer_text.delete("1.0", tk.END)
            
            answer_text = f"Answer:\n{result['answer']}\n"
            
            if result['sources']:
                answer_text += "\n" + "="*50 + "\n"
                answer_text += "Sources:\n"
                for i, source in enumerate(result['sources'], 1):
                    answer_text += f"\n[{i}] {source['metadata'].get('source', 'Unknown')}\n"
                    answer_text += f"{source['content'][:200]}...\n"
            
            if result['error']:
                answer_text += f"\n\nError: {result['error']}"
            
            self.answer_text.insert("1.0", answer_text)
            self.answer_text.config(state=tk.DISABLED)
            self.status_var.set("Ready")
        
        except Exception as e:
            self.answer_text.config(state=tk.NORMAL)
            self.answer_text.delete("1.0", tk.END)
            self.answer_text.insert("1.0", f"Error: {str(e)}")
            self.answer_text.config(state=tk.DISABLED)
            self.status_var.set("Error")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = RAGApplicationGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
