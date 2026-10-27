import customtkinter as ctk

# ---------- Cores ----------
COR_FUNDO = "#0b0d12"
COR_ESQUERDA = "#0f2d36"
COR_CAMPO = "#0f1218"
COR_BORDA = "#272b35"
COR_TEXTO_SUAVE = "#8b93a1"
COR_HOVER_CAMPO = "#161a22"

CORES_DESTAQUE = [
    ("Verde-água", "#00bfa5"),
    ("Azul", "#3b82f6"),
    ("Roxo", "#8b5cf6"),
    ("Laranja", "#f97316"),
]

FERRAMENTAS = [
    ("Google Drive", "Arquivos e documentos"),
    ("GitHub", "Repositórios e commits"),
    ("Slack", "Mensagens da equipe"),
    ("Notion", "Notas e tarefas"),
]

# "Banco de dados" em memória (some quando fechar o programa)
usuarios = {"admin@admin.com": {"nome": "Admin", "senha": "12345678"}}

ctk.set_appearance_mode("dark")


# ---------- Funções de cor ----------
def mistura(a, b, t):
    """Mistura duas cores hex. t vai de 0 (cor a) até 1 (cor b)."""
    ar, ag, ab = int(a[1:3], 16), int(a[3:5], 16), int(a[5:7], 16)
    br, bg, bb = int(b[1:3], 16), int(b[3:5], 16), int(b[5:7], 16)
    r = round(ar + (br - ar) * t)
    g = round(ag + (bg - ag) * t)
    bl = round(ab + (bb - ab) * t)
    return "#%02x%02x%02x" % (r, g, bl)


def escurecer(cor, fator=0.82):
    r, g, b = int(cor[1:3], 16), int(cor[3:5], 16), int(cor[5:7], 16)
    return "#%02x%02x%02x" % (int(r * fator), int(g * fator), int(b * fator))


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Bem-vindo")
        self.geometry("1000x680")
        self.resizable(False, False)
        self.configure(fg_color=COR_FUNDO)

        # Estado do programa
        self.cor = CORES_DESTAQUE[0][1]
        self.cor_hover = escurecer(self.cor)
        self.passo = 0
        self.anim_id = 0
        self.nome_usuario = ""
        self.ferramentas = {nome: False for nome, _ in FERRAMENTAS}
        self.espaco = ""
        self.layout = "Confortável"
        self.senha_visivel = False

        self.construir_esquerda()

        self.direita = ctk.CTkFrame(self, fg_color=COR_FUNDO, corner_radius=0)
        self.direita.pack(side="right", fill="both", expand=True)

        self.mostrar_cadastro()

    # =====================================================
    #                    LADO ESQUERDO
    # =====================================================
    def estado_alvo(self, i):
        """Cores que o cartão do passo i deve ter agora."""
        if self.passo > i:  # concluído
            return {"bg": COR_ESQUERDA, "txt": "#ffffff", "circ": self.cor}
        if self.passo == i:  # ativo
            return {"bg": "#ffffff", "txt": "#0b0d12", "circ": "#0b0d12"}
        return {"bg": COR_ESQUERDA, "txt": "#8fa6ad", "circ": "#1c3f4a"}  # pendente

    def construir_esquerda(self):
        esquerda = ctk.CTkFrame(self, fg_color=COR_ESQUERDA, corner_radius=0, width=420)
        esquerda.pack(side="left", fill="y")
        esquerda.pack_propagate(False)

        ctk.CTkLabel(
            esquerda,
            text="Bem-vindo ao Sistema",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#ffffff",
        ).pack(anchor="w", padx=36, pady=(60, 0))

        ctk.CTkLabel(
            esquerda,
            text="Siga os passos para ativar seu espaço de trabalho.",
            font=ctk.CTkFont(size=13),
            text_color=COR_TEXTO_SUAVE,
        ).pack(anchor="w", padx=36, pady=(4, 36))

        nomes_passos = [
            "Crie sua conta",
            "Conecte suas ferramentas",
            "Personalize seu painel",
        ]
        self.cartoes = []
        self.visual = []

        for i, texto in enumerate(nomes_passos):
            alvo = self.estado_alvo(i)
            cartao = ctk.CTkFrame(
                esquerda, fg_color=alvo["bg"], corner_radius=12, height=50
            )
            cartao.pack(fill="x", padx=28, pady=4)
            cartao.pack_propagate(False)

            circulo = ctk.CTkLabel(
                cartao,
                text=str(i + 1),
                width=28,
                height=28,
                corner_radius=14,
                fg_color=alvo["circ"],
                text_color="#ffffff",
                font=ctk.CTkFont(size=12, weight="bold"),
            )
            circulo.pack(side="left", padx=(14, 12))

            rotulo = ctk.CTkLabel(
                cartao,
                text=texto,
                font=ctk.CTkFont(size=14),
                text_color=alvo["txt"],
            )
            rotulo.pack(side="left")

            self.cartoes.append(
                {"cartao": cartao, "circulo": circulo, "rotulo": rotulo}
            )
            self.visual.append(dict(alvo))

        # Barra de progresso embaixo
        base = ctk.CTkFrame(esquerda, fg_color="transparent")
        base.pack(side="bottom", fill="x", padx=36, pady=40)

        self.label_progresso = ctk.CTkLabel(
            base,
            text="Passo 1 de 3",
            font=ctk.CTkFont(size=12),
            text_color=COR_TEXTO_SUAVE,
        )
        self.label_progresso.pack(anchor="w", pady=(0, 8))

        self.barra = ctk.CTkProgressBar(
            base, height=8, corner_radius=4, fg_color="#1c3f4a", progress_color=self.cor
        )
        self.barra.pack(fill="x")
        self.barra.set(1 / 3)
        self.progresso_atual = 1 / 3

    def ir_para_passo(self, passo):
        """Anima os cartões e a barra para o passo indicado."""
        self.passo = passo
        self.anim_id += 1
        meu_id = self.anim_id

        alvos = [self.estado_alvo(i) for i in range(3)]
        inicios = [dict(v) for v in self.visual]
        progresso_ini = self.progresso_atual
        progresso_fim = 1.0 if passo >= 3 else (passo + 1) / 3

        # Números viram ✓ nos passos concluídos
        for i in range(3):
            feito = passo > i
            self.cartoes[i]["circulo"].configure(text="✓" if feito else str(i + 1))

        self.label_progresso.configure(
            text="Tudo pronto! 🎉" if passo >= 3 else f"Passo {passo + 1} de 3"
        )
        self.barra.configure(progress_color=self.cor)

        total = 14

        def quadro(k):
            if meu_id != self.anim_id:
                return
            t = k / total
            e = 1 - (1 - t) ** 3  # animação suave (ease-out)

            for i in range(3):
                for chave in ("bg", "txt", "circ"):
                    self.visual[i][chave] = mistura(
                        inicios[i][chave], alvos[i][chave], e
                    )
                self.cartoes[i]["cartao"].configure(fg_color=self.visual[i]["bg"])
                self.cartoes[i]["rotulo"].configure(text_color=self.visual[i]["txt"])
                self.cartoes[i]["circulo"].configure(fg_color=self.visual[i]["circ"])

            self.progresso_atual = progresso_ini + (progresso_fim - progresso_ini) * e
            self.barra.set(self.progresso_atual)

            if k < total:
                self.after(18, lambda: quadro(k + 1))

        quadro(1)

    # =====================================================
    #                    UTILIDADES
    # =====================================================
    def limpar_direita(self):
        for widget in self.direita.winfo_children():
            widget.destroy()
        self.container = ctk.CTkFrame(self.direita, fg_color="transparent", width=360)
        self.container.place(relx=0.5, rely=0.5, anchor="center")

    def titulo(self, texto, subtitulo):
        ctk.CTkLabel(
            self.container,
            text=texto,
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#ffffff",
        ).pack(anchor="w")
        ctk.CTkLabel(
            self.container,
            text=subtitulo,
            font=ctk.CTkFont(size=13),
            text_color=COR_TEXTO_SUAVE,
        ).pack(anchor="w", pady=(2, 20))

    def campo(self, parent, placeholder, **kwargs):
        return ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            height=40,
            corner_radius=10,
            fg_color=COR_CAMPO,
            border_color=COR_BORDA,
            border_width=1,
            **kwargs,
        )

    def rotulo(self, parent, texto):
        return ctk.CTkLabel(
            parent,
            text=texto,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#ffffff",
        )

    def botao_principal(self, texto, comando):
        botao = ctk.CTkButton(
            self.container,
            text=texto,
            height=42,
            corner_radius=10,
            fg_color=self.cor,
            hover_color=self.cor_hover,
            text_color="#ffffff",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=comando,
        )
        botao.pack(fill="x", pady=(14, 0))
        return botao

    def link(self, parent, texto, comando, cor=None):
        return ctk.CTkButton(
            parent,
            text=texto,
            width=10,
            height=18,
            fg_color="transparent",
            hover_color=COR_FUNDO,
            text_color=cor or self.cor,
            font=ctk.CTkFont(size=12),
            command=comando,
        )

    def mensagem(self, texto, cor):
        self.label_msg.configure(text=texto, text_color=cor)

    def rodape(self, texto, link, comando):
        linha = ctk.CTkFrame(self.container, fg_color="transparent")
        linha.pack(pady=(14, 0))
        ctk.CTkLabel(
            linha, text=texto, font=ctk.CTkFont(size=12), text_color=COR_TEXTO_SUAVE
        ).pack(side="left")
        self.link(linha, link, comando).pack(side="left")

    def botoes_sociais(self):
        linha = ctk.CTkFrame(self.container, fg_color="transparent")
        linha.pack(fill="x")
        linha.grid_columnconfigure((0, 1), weight=1, uniform="a")

        for coluna, nome in enumerate(["Google", "GitHub"]):
            ctk.CTkButton(
                linha,
                text=nome,
                height=38,
                corner_radius=10,
                fg_color="transparent",
                border_width=1,
                border_color=COR_BORDA,
                hover_color=COR_HOVER_CAMPO,
                command=lambda n=nome: self.mensagem(
                    f"Login com {n} em breve", "orange"
                ),
            ).grid(
                row=0,
                column=coluna,
                padx=(0, 6) if coluna == 0 else (6, 0),
                sticky="ew",
            )

        divisor = ctk.CTkFrame(self.container, fg_color="transparent")
        divisor.pack(fill="x", pady=16)
        divisor.grid_columnconfigure((0, 2), weight=1)
        ctk.CTkFrame(divisor, height=1, fg_color=COR_BORDA).grid(
            row=0, column=0, sticky="ew"
        )
        ctk.CTkLabel(
            divisor,
            text="  Ou continue com e-mail  ",
            font=ctk.CTkFont(size=11),
            text_color=COR_TEXTO_SUAVE,
        ).grid(row=0, column=1)
        ctk.CTkFrame(divisor, height=1, fg_color=COR_BORDA).grid(
            row=0, column=2, sticky="ew"
        )

    def campo_senha(self, placeholder):
        quadro = ctk.CTkFrame(self.container, fg_color="transparent")
        quadro.pack(fill="x")
        self.entrada_senha = self.campo(quadro, placeholder, show="•")
        self.entrada_senha.pack(fill="x")
        self.botao_olho = ctk.CTkButton(
            quadro,
            text="👁",
            width=30,
            height=28,
            fg_color=COR_CAMPO,
            hover_color=COR_HOVER_CAMPO,
            text_color=COR_TEXTO_SUAVE,
            command=self.alternar_senha,
        )
        self.botao_olho.place(relx=1.0, x=-8, rely=0.5, anchor="e")
        self.senha_visivel = False

    def alternar_senha(self):
        self.senha_visivel = not self.senha_visivel
        self.entrada_senha.configure(show="" if self.senha_visivel else "•")

    # =====================================================
    #              PASSO 1 - CRIAR CONTA / ENTRAR
    # =====================================================
    def mostrar_cadastro(self):
        self.ir_para_passo(0)
        self.limpar_direita()
        self.titulo("Crie sua conta", "Preencha seus dados para começar.")
        self.botoes_sociais()

        nomes = ctk.CTkFrame(self.container, fg_color="transparent")
        nomes.pack(fill="x")
        nomes.grid_columnconfigure((0, 1), weight=1, uniform="b")

        self.rotulo(nomes, "Nome").grid(row=0, column=0, sticky="w")
        self.rotulo(nomes, "Sobrenome").grid(row=0, column=1, sticky="w", padx=(6, 0))
        self.entrada_nome = self.campo(nomes, "Maria")
        self.entrada_nome.grid(row=1, column=0, sticky="ew", padx=(0, 6), pady=(4, 0))
        self.entrada_sobrenome = self.campo(nomes, "Silva")
        self.entrada_sobrenome.grid(
            row=1, column=1, sticky="ew", padx=(6, 0), pady=(4, 0)
        )

        self.rotulo(self.container, "E-mail").pack(anchor="w", pady=(12, 4))
        self.entrada_email = self.campo(self.container, "maria@exemplo.com")
        self.entrada_email.pack(fill="x")

        self.rotulo(self.container, "Senha").pack(anchor="w", pady=(12, 4))
        self.campo_senha("Digite sua senha")

        ctk.CTkLabel(
            self.container,
            text="A senha deve ter no mínimo 8 caracteres.",
            font=ctk.CTkFont(size=11),
            text_color=COR_TEXTO_SUAVE,
        ).pack(anchor="w", pady=(4, 0))

        self.botao_principal("Criar conta", self.criar_conta)

        self.label_msg = ctk.CTkLabel(
            self.container, text="", font=ctk.CTkFont(size=12)
        )
        self.label_msg.pack(pady=(8, 0))

        self.rodape("Já tem uma conta?", "Entrar", self.mostrar_login)

    def criar_conta(self):
        nome = self.entrada_nome.get().strip()
        sobrenome = self.entrada_sobrenome.get().strip()
        email = self.entrada_email.get().strip().lower()
        senha = self.entrada_senha.get()

        if not nome or not sobrenome or not email or not senha:
            self.mensagem("Preencha todos os campos.", "red")
        elif "@" not in email or "." not in email:
            self.mensagem("E-mail inválido.", "red")
        elif len(senha) < 8:
            self.mensagem("A senha deve ter no mínimo 8 caracteres.", "red")
        elif email in usuarios:
            self.mensagem("Esse e-mail já está cadastrado.", "red")
        else:
            usuarios[email] = {"nome": nome, "senha": senha}
            self.nome_usuario = nome
            self.mensagem("Conta criada com sucesso! Indo para o passo 2...", "#00e676")
            self.after(1000, self.mostrar_passo2)

    def mostrar_login(self):
        self.ir_para_passo(0)
        self.limpar_direita()
        self.titulo("Entrar", "Acesse sua conta para continuar.")
        self.botoes_sociais()

        self.rotulo(self.container, "E-mail").pack(anchor="w", pady=(0, 4))
        self.entrada_email = self.campo(self.container, "maria@exemplo.com")
        self.entrada_email.pack(fill="x")

        self.rotulo(self.container, "Senha").pack(anchor="w", pady=(12, 4))
        self.campo_senha("Digite sua senha")

        self.botao_principal("Entrar", self.entrar)

        self.label_msg = ctk.CTkLabel(
            self.container, text="", font=ctk.CTkFont(size=12)
        )
        self.label_msg.pack(pady=(8, 0))

        self.rodape("Ainda não tem conta?", "Criar conta", self.mostrar_cadastro)

    def entrar(self):
        email = self.entrada_email.get().strip().lower()
        senha = self.entrada_senha.get()

        usuario = usuarios.get(email)
        if usuario and usuario["senha"] == senha:
            self.nome_usuario = usuario["nome"]
            self.mensagem(f"Olá, {usuario['nome']}! Indo para o passo 2...", "#00e676")
            self.after(1000, self.mostrar_passo2)
        else:
            self.mensagem("E-mail ou senha incorretos.", "red")

    # =====================================================
    #              PASSO 2 - CONECTAR FERRAMENTAS
    # =====================================================
    def mostrar_passo2(self):
        self.ir_para_passo(1)
        self.limpar_direita()
        self.titulo("Conecte suas ferramentas", "Ligue as que você usa no dia a dia.")

        for nome, descricao in FERRAMENTAS:
            linha = ctk.CTkFrame(
                self.container,
                fg_color=COR_CAMPO,
                border_color=COR_BORDA,
                border_width=1,
                corner_radius=12,
                height=58,
            )
            linha.pack(fill="x", pady=4)
            linha.pack_propagate(False)

            textos = ctk.CTkFrame(linha, fg_color="transparent")
            textos.pack(side="left", padx=14)

            ctk.CTkLabel(
                textos,
                text=nome,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#ffffff",
            ).pack(anchor="w")

            lbl_desc = ctk.CTkLabel(
                textos,
                text=descricao,
                font=ctk.CTkFont(size=11),
                text_color=COR_TEXTO_SUAVE,
            )
            lbl_desc.pack(anchor="w")

            chave = ctk.CTkSwitch(linha, text="", width=40, progress_color=self.cor)
            chave.pack(side="right", padx=14)
            chave.configure(
                command=lambda n=nome, d=descricao, s=chave, l=lbl_desc: self.alternar_ferramenta(
                    n, d, s, l
                )
            )

            if self.ferramentas[nome]:
                chave.select()
                lbl_desc.configure(text="Conectado ✓", text_color=self.cor)

        self.label_contador = ctk.CTkLabel(
            self.container,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=COR_TEXTO_SUAVE,
        )
        self.label_contador.pack(anchor="w", pady=(8, 0))
        self.atualizar_contador()

        self.botao_principal("Continuar", self.mostrar_passo3)

        linha = ctk.CTkFrame(self.container, fg_color="transparent")
        linha.pack(fill="x", pady=(14, 0))
        self.link(linha, "← Voltar", self.mostrar_cadastro, COR_TEXTO_SUAVE).pack(
            side="left"
        )
        self.link(linha, "Pular por agora", self.mostrar_passo3, COR_TEXTO_SUAVE).pack(
            side="right"
        )

    def alternar_ferramenta(self, nome, descricao, chave, rotulo):
        ligado = chave.get() == 1
        self.ferramentas[nome] = ligado
        if ligado:
            rotulo.configure(text="Conectado ✓", text_color=self.cor)
        else:
            rotulo.configure(text=descricao, text_color=COR_TEXTO_SUAVE)
        self.atualizar_contador()

    def atualizar_contador(self):
        total = sum(1 for v in self.ferramentas.values() if v)
        self.label_contador.configure(
            text=f"{total} de {len(self.ferramentas)} ferramentas conectadas",
            text_color=self.cor if total else COR_TEXTO_SUAVE,
        )

    # =====================================================
    #              PASSO 3 - PERSONALIZAR PAINEL
    # =====================================================
    def mostrar_passo3(self):
        self.ir_para_passo(2)
        self.limpar_direita()
        self.titulo("Personalize seu painel", "Deixe com a sua cara.")

        self.rotulo(self.container, "Nome do espaço de trabalho").pack(
            anchor="w", pady=(0, 4)
        )
        self.entrada_espaco = self.campo(self.container, "Meu espaço")
        self.entrada_espaco.pack(fill="x")
        self.entrada_espaco.insert(0, self.espaco or f"Espaço de {self.nome_usuario}")

        self.rotulo(self.container, "Cor de destaque").pack(anchor="w", pady=(16, 8))
        cores = ctk.CTkFrame(self.container, fg_color="transparent")
        cores.pack(anchor="w")
        for nome_cor, hexa in CORES_DESTAQUE:
            selecionada = hexa == self.cor
            ctk.CTkButton(
                cores,
                text="✓" if selecionada else "",
                width=42,
                height=42,
                corner_radius=21,
                fg_color=hexa,
                hover_color=escurecer(hexa),
                border_width=3 if selecionada else 0,
                border_color="#ffffff",
                text_color="#ffffff",
                font=ctk.CTkFont(size=16, weight="bold"),
                command=lambda h=hexa: self.trocar_cor(h),
            ).pack(side="left", padx=(0, 10))

        self.rotulo(self.container, "Layout").pack(anchor="w", pady=(16, 8))
        seletor = ctk.CTkSegmentedButton(
            self.container,
            values=["Confortável", "Compacto"],
            fg_color=COR_CAMPO,
            selected_color=self.cor,
            selected_hover_color=self.cor_hover,
            unselected_color=COR_CAMPO,
            unselected_hover_color=COR_HOVER_CAMPO,
            height=38,
            command=self.trocar_layout,
        )
        seletor.set(self.layout)
        seletor.pack(fill="x")

        self.botao_principal("Concluir", self.concluir)

        linha = ctk.CTkFrame(self.container, fg_color="transparent")
        linha.pack(fill="x", pady=(14, 0))
        self.link(linha, "← Voltar", self.mostrar_passo2, COR_TEXTO_SUAVE).pack(
            side="left"
        )

    def trocar_cor(self, hexa):
        self.espaco = self.entrada_espaco.get()
        self.cor = hexa
        self.cor_hover = escurecer(hexa)
        self.mostrar_passo3()

    def trocar_layout(self, valor):
        self.layout = valor

    def concluir(self):
        self.espaco = (
            self.entrada_espaco.get().strip() or f"Espaço de {self.nome_usuario}"
        )
        self.mostrar_final()

    # =====================================================
    #                      TELA FINAL
    # =====================================================
    def mostrar_final(self):
        self.ir_para_passo(3)
        self.limpar_direita()

        ctk.CTkLabel(self.container, text="🎉", font=ctk.CTkFont(size=56)).pack()
        ctk.CTkLabel(
            self.container,
            text=f"Tudo pronto, {self.nome_usuario}!",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#ffffff",
        ).pack(pady=(8, 0))
        ctk.CTkLabel(
            self.container,
            text="Seu espaço de trabalho foi ativado.",
            font=ctk.CTkFont(size=13),
            text_color=COR_TEXTO_SUAVE,
        ).pack(pady=(2, 20))

        conectadas = [n for n, v in self.ferramentas.items() if v]
        resumo = [
            ("Espaço", self.espaco),
            ("Ferramentas", ", ".join(conectadas) if conectadas else "Nenhuma"),
            ("Layout", self.layout),
        ]

        cartao = ctk.CTkFrame(
            self.container,
            fg_color=COR_CAMPO,
            border_color=self.cor,
            border_width=1,
            corner_radius=12,
        )
        cartao.pack(fill="x")
        for titulo, valor in resumo:
            linha = ctk.CTkFrame(cartao, fg_color="transparent")
            linha.pack(fill="x", padx=16, pady=8)
            ctk.CTkLabel(
                linha,
                text=titulo,
                font=ctk.CTkFont(size=12),
                text_color=COR_TEXTO_SUAVE,
            ).pack(side="left")
            ctk.CTkLabel(
                linha,
                text=valor,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#ffffff",
                wraplength=220,
                justify="right",
            ).pack(side="right")

        self.botao_principal("Recomeçar", self.recomecar)

    def recomecar(self):
        self.nome_usuario = ""
        self.ferramentas = {nome: False for nome, _ in FERRAMENTAS}
        self.espaco = ""
        self.layout = "Confortável"
        self.mostrar_cadastro()


if __name__ == "__main__":
    app = App()
    app.mainloop()
