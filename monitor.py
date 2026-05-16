import psutil
import platform
import os
from datetime import datetime
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.columns import Columns

console = Console()

class CyberToolbox:
    def __init__(self):
        self.layout = Layout()
        self.split_screen()

    def split_screen(self):
        # Divide a tela em Topo, Meio (Monitor + Rede) e Baixo (Arquivos)
        self.layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main", size=12),
            Layout(name="footer")
        )
        self.layout["main"].split_row(
            Layout(name="monitor"),
            Layout(name="network")
        )

    def get_sys_info(self):
        # Informações da Máquina
        info = f"[bold white]OS:[/] {platform.system()} {platform.release()}\n"
        info += f"[bold white]Node:[/] {platform.node()}\n"
        info += f"[bold white]CPU:[/] {psutil.cpu_count()} Núcleos"
        return Panel(info, title="💻 Sistema", border_style="magenta")

    def get_network_info(self):
        # Pega o IP e status da rede
        interfaces = psutil.net_if_addrs()
        net_info = ""
        for name, addrs in interfaces.items():
            for addr in addrs:
                if addr.family == 2: # IPv4
                    net_info += f"🌐 [bold]{name}[/]: {addr.address}\n"
        
        return Panel(net_info or "Sem conexão ativa", title="📡 Rede", border_style="green")

    def get_file_explorer(self):
        # Lista arquivos na pasta atual para mostrar que você mexe com I/O
        files = os.listdir('.')[:10] # Primeiros 10 arquivos
        file_table = Table(title="📂 Explorador de Arquivos (Pasta Atual)", expand=True)
        file_table.add_column("Nome", style="cyan")
        file_table.add_column("Tamanho (KB)", justify="right")

        for f in files:
            size = os.path.getsize(f) // 1024
            file_table.add_row(f, str(size))
            
        return Panel(file_table, border_style="yellow")

    def render(self):
        hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.layout["header"].update(Panel(f"[bold yellow]ADMIN TOOLBOX[/] | {hora}", textAlign="center"))
        self.layout["monitor"].update(self.get_sys_info())
        self.layout["network"].update(self.get_network_info())
        self.layout["footer"].update(self.get_file_explorer())
        return self.layout

if __name__ == "__main__":
    app = CyberToolbox()
    try:
        with Live(app.render(), refresh_per_second=1, screen=True) as live:
            while True:
                import time
                time.sleep(1)
                live.update(app.render())
    except KeyboardInterrupt:
        console.print("[bold red]\nDesligando central de controle...[/]")