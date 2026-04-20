from json import tool

from Core import inface


class ToolClassRoot:
    kit_name:str = "undefined"
    tool_name:str = "undefined"
    @staticmethod
    def run(opt:str)->None:
        pass

    @staticmethod
    def man()->None:
        pass


class Worker:
    tools:dict[str,dict[str,type[ToolClassRoot]]] = {}
    tool:str = "";

    @staticmethod
    def work(args: list[str]) -> None:
        while True:
            Worker.kit_pick(args)
            inface.input("\n")
            args = []

    @staticmethod
    def kit_pick(args: list[str]) -> None:
        kits = list(Worker.tools.keys())

        # --- Résolution du kit ---
        if len(args) >= 1:
            kit_name = args[0]
            if kit_name in Worker.tools:
                Worker.tool_pick(kit_name, Worker.tools[kit_name], args)
                return
            else:
                print(f"Kit '{kit_name}' introuvable.")


        kit_name = inface.choice("tK", kits, sentence="Choose the toolKit :")
        print(f"\n<===== ToolKit : {kit_name} =====>\n")
        Worker.tool_pick(kit_name, Worker.tools[kit_name], args)

    @staticmethod
    def tool_pick(kit_name:str, kit: dict[str,type[ToolClassRoot]], args: list[str]) -> None:

        # --- Résolution du tool ---
        tool_names = list(kit.keys())

        if len(args) >= 2:
            tool_name = args[1]
            if tool_name.isdigit():
                idx = int(tool_name)
                if 0 <= idx < len(tool_names):
                    tool_name = tool_names[idx]
                else:
                    print(f"Numéro de tool invalide.")
                    return
            if tool_name not in kit:
                print(f"Tool '{tool_name}' introuvable.")
                Worker.tool_pick(kit_name, kit, args)
                return
        else:
            tool_name = inface.choice("T", tool_names, True, f"{kit_name} toolKit's tools ('b' to change toolKit):")
            if tool_name is None:
                Worker.kit_pick([])
                return

        print(f"\n<=== Tool : {kit_name}.{tool_name} ===>\n")

        Worker.option_pick(kit[tool_name], args)

    @staticmethod
    def option_pick(tool:type[ToolClassRoot],args:list[str]) -> None:
        # --- Résolution des options ---
        man_flags = {"-h", "-help", "-man", "h", "help", "man"}

        if len(args) > 2:
            opts = args[2]
        else:
            # Aucune option fournie → prompt (sauf si l'utilisateur a passé "-" seul)
            opts = inface.input("options (h for help, 'back' to change Tool): \n>>").strip()

        # Flags spéciaux → man()
        if opts in man_flags:
            tool.man()
            Worker.option_pick(tool, [])
            return
        if opts.lower()=="back":
            Worker.tool_pick(tool.kit_name, Worker.tools[tool.kit_name], [])
            return
        tool.run(opts)


def tool_def(kit_name_a:str, tool_name_a:str):
    def tc(t_class:object):
        class ToolClass(t_class, ToolClassRoot):
             kit_name:str = kit_name_a
             tool_name:str = tool_name_a
        if Worker.tools.get(kit_name_a) is None:
            Worker.tools[kit_name_a] = {}
        Worker.tools[kit_name_a][tool_name_a] = ToolClass
        return ToolClass
    return tc