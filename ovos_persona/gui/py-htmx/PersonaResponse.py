from pyhtmx import Div, Button, Style, Script
from pyhtmx_gui.kit import Page, SessionItem, Control

class PersonaResponsePage(Page):
    _parameters = ("title", "text")

    def __init__(self, session_data=None):
        session_data = session_data or {}
        super().__init__(name="persona-response-page", session_data=session_data)
        self.speech_history = []

        # 1. De Orb Container (v4 structuur)
        self.orb_visual = Div([
            Div([
                Div(_id="l1", _class="plasma p1"),
                Div(_id="l2", _class="plasma p2"),
                Div(_id="l3", _class="plasma p3"),
                Div(_class="glass-overlay")
            ], _id="orb", _class="orb-outer")
        ], _class="canvas")

        # 2. CSS (v4 styling)
        self.custom_style = Style("""
            .canvas { width: 100%; height: 320px; display: flex; justify-content: center; align-items: center; }
            .orb-outer {
                position: relative; width: 190px; height: 240px;
                border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
                display: flex; justify-content: center; align-items: center;
                filter: drop-shadow(0 0 35px rgba(108, 92, 231, 0.5));
                will-change: transform;
                background: #000;
            }
            .plasma {
                position: absolute; width: 100%; height: 100%;
                border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
                mix-blend-mode: screen; will-change: transform, border-radius, opacity;
            }
            .p1 { background: radial-gradient(circle at 30% 30%, #6c5ce7, transparent); animation: rotate 10s infinite linear; }
            .p2 { background: radial-gradient(circle at 70% 60%, #02ffc0, transparent); animation: rotate 15s infinite linear reverse; }
            .p3 { background: radial-gradient(circle at 40% 80%, #fd79a8, transparent); animation: rotate 12s infinite linear; }
            .glass-overlay {
                position: absolute; width: 100%; height: 100%;
                border-radius: inherit;
                background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.1), transparent 60%);
                box-shadow: inset -5px -5px 15px rgba(0,0,0,0.5), inset 5px 5px 15px rgba(255,255,255,0.05);
                z-index: 10;
            }
            @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        """)

        # 3. JS: Exacte v4 Animatie Logica
        self.orb_script = Script("""
            (function() {
                const orb = document.getElementById('orb');
                const layers = [document.getElementById('l1'), document.getElementById('l2'), document.getElementById('l3')];
                let isSpeaking = false;
                let lerpScale = 1;
                let lerpValues = [0, 0, 0];
                const smoothness = 0.08;

                document.addEventListener('ovos.speak', () => { isSpeaking = true; });
                document.addEventListener('ovos.speak.finished', () => { isSpeaking = false; });

                function lerp(start, end, amt) { return (1 - amt) * start + amt * end; }

                function draw() {
                    requestAnimationFrame(draw);
                    // Simulatie van audiofrequenties uit v4
                    const freqBase = isSpeaking ? (Math.sin(Date.now() * 0.01) * 50 + 150) : 0;
                    
                    const targetScale = 1 + (freqBase / 500);
                    lerpScale = lerp(lerpScale, targetScale, smoothness);
                    if(orb) orb.style.transform = `scale(${lerpScale})`;

                    layers.forEach((layer, i) => {
                        if(!layer) return;
                        const targetVal = isSpeaking ? (freqBase * (1 - i * 0.15) + (Math.random() * 20)) : 0;
                        lerpValues[i] = lerp(lerpValues[i], targetVal, smoothness);
                        const v = lerpValues[i];
                        
                        const v1 = 50 + (v / 40);
                        const v2 = 50 - (v / 40);
                        layer.style.borderRadius = `${v1}% ${v2}% ${v1}% ${v2}% / ${60+(v/50)}% ${60+(v/50)}% ${40-(v/50)}% ${40-(v/50)}%`;
                        layer.style.opacity = isSpeaking ? (0.4 + (v / 400)) : 0.4;
                    });
                }
                draw();
            })();
        """)

        # UI Elementen
        title = Div(inner_content=session_data.get("title", "Persona"), _class="text-[4vw] font-bold text-gray-100")
        self.response_text_div = Div(inner_content="", _id="persona-text", _class="text-[3vw] font-semibold text-gray-300 mt-4 text-center italic")

        # Event Handlers
        self.add_interaction("on_speak", Control(event="speak", callback=self._on_status_handler_speak, context="global"))
        self.add_interaction("on_reset", Control(event="recognizer_loop:utterance", callback=self._reset_display, context="global"))

        self._button = Button("Back to Home", _id="btn-close", _class="btn btn-outline border-2 border-blue-400 text-blue-400 font-bold py-2 px-6 rounded-full mt-8")
        self.add_interaction("btn-close-click", Control(context="global", event="click", callback=lambda r, _: r.close(), source=self._button))

        # Container (Zwart)
        container = Div(
            [self.custom_style, self.orb_visual, title, self.response_text_div, self._button, self.orb_script],
            _class="p-[4vw] flex flex-col items-center justify-start rounded-2xl shadow-2xl bg-gray-900",
            style={"width": "80vw", "height": "80vh"}
        )

        self._page = Div(container, _class="flex items-center justify-center min-h-screen w-full", style={"background": "linear-gradient(to right, #3b82f6, #ffb6c1)"})

    def _on_status_handler_speak(self, renderer, message):
        new_text = message.data.get("speech")
        if new_text and isinstance(new_text, str):
            clean_text = new_text.strip()
            if clean_text and clean_text not in self.speech_history:
                self.speech_history.append(clean_text)
                self.response_text_div.inner_content = " ".join(self.speech_history)
                renderer.update(self.response_text_div)

    def _reset_display(self, renderer, message=None):
        self.speech_history = []
        self.response_text_div.inner_content = ""
        renderer.update(self.response_text_div)

    def build(self): return self._page