const API_BASE_URL =
    "https://raio-x-politico-api.onrender.com/api";

const elementos = {
    lista: document.querySelector("#deputados-lista"),
    resultadoCount: document.querySelector("#resultado-count"),
    busca: document.querySelector("#search"),
    botaoBusca: document.querySelector("#search-button"),
    totalDeputados: document.querySelector("#total-deputados"),
    totalDespesas: document.querySelector("#total-despesas"),
    totalPartidos: document.querySelector("#total-partidos"),
};


let deputados = [];


/* =========================
   API
   ========================= */

async function buscarDeputados() {
    const resposta = await fetch(
        `${API_BASE_URL}/deputados`
    );

    if (!resposta.ok) {
        throw new Error(
            `Erro HTTP: ${resposta.status}`
        );
    }

    return resposta.json();
}


/* =========================
   UTILITÁRIOS
   ========================= */

function obterIniciais(nome) {
    return nome
        .trim()
        .split(/\s+/)
        .slice(0, 2)
        .map(parte => parte[0])
        .join("")
        .toUpperCase();
}


function escaparHTML(valor) {
    return String(valor)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


/* =========================
   RENDERIZAÇÃO
   ========================= */

function renderizarDeputados(lista) {

    if (lista.length === 0) {

        elementos.lista.innerHTML = `
            <div class="loading">
                Nenhum deputado encontrado.
            </div>
        `;

        elementos.resultadoCount.textContent =
            "Nenhum resultado";

        return;
    }


    elementos.lista.innerHTML = lista
        .map(deputado => {

            const nome = escaparHTML(
                deputado.nome
            );

            const partido = escaparHTML(
                deputado.partido || "Sem partido"
            );

            const uf = escaparHTML(
                deputado.uf || "--"
            );

            const iniciais = obterIniciais(
                deputado.nome
            );


            return `
                <a
                    class="deputado-card"
                    href="/web/deputado.html?id=${deputado.id_camara}"
                >
                    <div class="deputado-card-header">

                        <div class="deputado-avatar">
                            ${iniciais}
                        </div>

                        <div>
                            <div class="deputado-name">
                                ${nome}
                            </div>

                            <div class="deputado-meta">
                                ${partido} • ${uf}
                            </div>
                        </div>

                    </div>
                </a>
            `;
        })
        .join("");


    elementos.resultadoCount.textContent =
        `${lista.length} deputado${lista.length !== 1 ? "s" : ""}`;
}


function atualizarEstatisticas() {

    elementos.totalDeputados.textContent =
        deputados.length.toLocaleString("pt-BR");


    elementos.totalPartidos.textContent =
        new Set(
            deputados
                .map(deputado => deputado.partido)
                .filter(Boolean)
        ).size.toLocaleString("pt-BR");
}


/* =========================
   BUSCA
   ========================= */

function filtrarDeputados() {

    const termo = elementos.busca.value
        .trim()
        .toLowerCase();


    if (!termo) {

        renderizarDeputados(
            deputados
        );

        return;
    }


    const resultados = deputados.filter(
        deputado => {

            const nome =
                deputado.nome?.toLowerCase() || "";

            const partido =
                deputado.partido?.toLowerCase() || "";

            const uf =
                deputado.uf?.toLowerCase() || "";


            return (
                nome.includes(termo) ||
                partido.includes(termo) ||
                uf.includes(termo)
            );
        }
    );


    renderizarDeputados(
        resultados
    );
}


/* =========================
   ESTADO DE ERRO
   ========================= */

function mostrarErro() {

    elementos.lista.innerHTML = `
        <div class="loading">
            Não foi possível carregar os deputados.
            <br>
            <small>
                Verifique se a API está funcionando.
            </small>
        </div>
    `;

    elementos.resultadoCount.textContent =
        "Erro ao carregar";
}


/* =========================
   INICIALIZAÇÃO
   ========================= */

async function iniciar() {

    try {

        const dados =
            await buscarDeputados();


        deputados =
            dados.deputados || [];


        atualizarEstatisticas();

        renderizarDeputados(
            deputados
        );


        console.log(
            `✅ ${deputados.length} deputados carregados`
        );

    } catch (erro) {

        console.error(
            "Erro ao carregar deputados:",
            erro
        );

        mostrarErro();
    }
}


/* =========================
   EVENTOS
   ========================= */

elementos.busca.addEventListener(
    "input",
    filtrarDeputados
);


elementos.botaoBusca.addEventListener(
    "click",
    () => {

        elementos.busca.focus();

        filtrarDeputados();
    }
);


iniciar();
