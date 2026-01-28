import json
from datetime import datetime
import os

class ToDoList:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()
    
    def load_tasks(self):
        """Muat tugas dari file JSON"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_tasks(self):
        """Simpan tugas ke file JSON"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, indent=2, ensure_ascii=False)
    
    def add_task(self, title, description="", due_date=""):
        """Tambah tugas baru"""
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "description": description,
            "due_date": due_date,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"✓ Tugas '{title}' berhasil ditambahkan!")
        return task
    
    def list_tasks(self, show_completed=True):
        """Tampilkan semua tugas"""
        if not self.tasks:
            print("📋 Belum ada tugas.")
            return
        
        print("\n" + "="*70)
        print(f"{'ID':<4} {'Status':<10} {'Judul':<20} {'Batas Waktu':<15} {'Deskripsi':<20}")
        print("="*70)
        
        for task in self.tasks:
            if not show_completed and task["completed"]:
                continue
            
            status = "✓ Selesai" if task["completed"] else "⧗ Aktif"
            due_date = task.get("due_date", "-")
            desc = task.get("description", "")[:20]
            
            print(f"{task['id']:<4} {status:<10} {task['title']:<20} {due_date:<15} {desc:<20}")
        
        print("="*70 + "\n")
    
    def complete_task(self, task_id):
        """Tandai tugas sebagai selesai"""
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                self.save_tasks()
                print(f"✓ Tugas '{task['title']}' ditandai selesai!")
                return
        print(f"✗ Tugas dengan ID {task_id} tidak ditemukan.")
    
    def delete_task(self, task_id):
        """Hapus tugas"""
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                title = task["title"]
                self.tasks.pop(i)
                self.save_tasks()
                print(f"✓ Tugas '{title}' berhasil dihapus!")
                return
        print(f"✗ Tugas dengan ID {task_id} tidak ditemukan.")
    
    def update_task(self, task_id, **kwargs):
        """Edit tugas"""
        for task in self.tasks:
            if task["id"] == task_id:
                for key, value in kwargs.items():
                    if key in task:
                        task[key] = value
                self.save_tasks()
                print(f"✓ Tugas '{task['title']}' berhasil diperbarui!")
                return
        print(f"✗ Tugas dengan ID {task_id} tidak ditemukan.")
    
    def view_task_details(self, task_id):
        """Lihat detail tugas"""
        for task in self.tasks:
            if task["id"] == task_id:
                print("\n" + "="*50)
                print(f"ID: {task['id']}")
                print(f"Judul: {task['title']}")
                print(f"Deskripsi: {task.get('description', '-')}")
                print(f"Batas Waktu: {task.get('due_date', '-')}")
                print(f"Status: {'✓ Selesai' if task['completed'] else '⧗ Aktif'}")
                print(f"Dibuat: {task.get('created_at', '-')}")
                print("="*50 + "\n")
                return
        print(f"✗ Tugas dengan ID {task_id} tidak ditemukan.")
    
    def get_active_tasks(self):
        """Dapatkan tugas yang belum selesai"""
        return [task for task in self.tasks if not task["completed"]]
    
    def get_completed_tasks(self):
        """Dapatkan tugas yang sudah selesai"""
        return [task for task in self.tasks if task["completed"]]


def print_menu():
    """Tampilkan menu utama"""
    print("\n" + "="*50)
    print("📝 APLIKASI TO-DO LIST")
    print("="*50)
    print("1. Lihat semua tugas")
    print("2. Tambah tugas baru")
    print("3. Tandai tugas selesai")
    print("4. Hapus tugas")
    print("5. Edit tugas")
    print("6. Lihat detail tugas")
    print("7. Lihat tugas aktif saja")
    print("8. Lihat tugas selesai saja")
    print("9. Keluar")
    print("="*50)


def main():
    """Fungsi utama aplikasi"""
    todo = ToDoList()
    
    while True:
        print_menu()
        choice = input("Pilih menu (1-9): ").strip()
        
        if choice == "1":
            print("\n📋 DAFTAR SEMUA TUGAS")
            todo.list_tasks()
        
        elif choice == "2":
            print("\n➕ TAMBAH TUGAS BARU")
            title = input("Judul tugas: ").strip()
            if title:
                description = input("Deskripsi (opsional): ").strip()
                due_date = input("Batas waktu (YYYY-MM-DD) (opsional): ").strip()
                todo.add_task(title, description, due_date)
            else:
                print("✗ Judul tugas tidak boleh kosong!")
        
        elif choice == "3":
            print("\n✓ TANDAI TUGAS SELESAI")
            todo.list_tasks()
            try:
                task_id = int(input("Masukkan ID tugas yang selesai: "))
                todo.complete_task(task_id)
            except ValueError:
                print("✗ Masukkan ID yang valid!")
        
        elif choice == "4":
            print("\n🗑️  HAPUS TUGAS")
            todo.list_tasks()
            try:
                task_id = int(input("Masukkan ID tugas yang akan dihapus: "))
                confirm = input("Yakin hapus? (y/n): ").strip().lower()
                if confirm == 'y':
                    todo.delete_task(task_id)
            except ValueError:
                print("✗ Masukkan ID yang valid!")
        
        elif choice == "5":
            print("\n✏️  EDIT TUGAS")
            todo.list_tasks()
            try:
                task_id = int(input("Masukkan ID tugas yang akan diedit: "))
                print("Apa yang ingin diedit?")
                print("1. Judul")
                print("2. Deskripsi")
                print("3. Batas waktu")
                edit_choice = input("Pilih (1-3): ").strip()
                
                if edit_choice == "1":
                    new_title = input("Judul baru: ").strip()
                    if new_title:
                        todo.update_task(task_id, title=new_title)
                elif edit_choice == "2":
                    new_desc = input("Deskripsi baru: ").strip()
                    todo.update_task(task_id, description=new_desc)
                elif edit_choice == "3":
                    new_date = input("Batas waktu baru (YYYY-MM-DD): ").strip()
                    todo.update_task(task_id, due_date=new_date)
                else:
                    print("✗ Pilihan tidak valid!")
            except ValueError:
                print("✗ Masukkan ID yang valid!")
        
        elif choice == "6":
            print("\n🔍 DETAIL TUGAS")
            todo.list_tasks()
            try:
                task_id = int(input("Masukkan ID tugas: "))
                todo.view_task_details(task_id)
            except ValueError:
                print("✗ Masukkan ID yang valid!")
        
        elif choice == "7":
            print("\n⧗ TUGAS AKTIF")
            active_tasks = todo.get_active_tasks()
            if active_tasks:
                print(f"\nJumlah tugas aktif: {len(active_tasks)}\n")
                for task in active_tasks:
                    print(f"[{task['id']}] {task['title']} (Batas: {task.get('due_date', '-')})")
            else:
                print("✓ Semua tugas sudah selesai!")
        
        elif choice == "8":
            print("\n✓ TUGAS SELESAI")
            completed_tasks = todo.get_completed_tasks()
            if completed_tasks:
                print(f"\nJumlah tugas selesai: {len(completed_tasks)}\n")
                for task in completed_tasks:
                    print(f"[{task['id']}] {task['title']}")
            else:
                print("Belum ada tugas yang selesai.")
        
        elif choice == "9":
            print("\n👋 Terima kasih telah menggunakan Aplikasi To-Do List!")
            break
        
        else:
            print("✗ Pilihan tidak valid! Coba lagi.")


if __name__ == "__main__":
    main()
