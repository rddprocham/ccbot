import colorama

def bold(text):
    return f"\033[1m{text}\033[0m"
def cogs_loaded(name, loaded=True):
    if loaded=="r":
        print(f"{prefix('cogs_other')} {name}.py reloaded!")
    elif loaded == True:
        print(f"{prefix('cogs_positive')} {name} cog loaded!")
    else:
        print(f"{prefix('cogs_negative')} {name} cog disabled, not loaded.")

def error(error_txt):
    print(f"{prefix('error')} {error_txt}")

def prefix(prefix):
    prefixes={
        "cogs_positive":["COGS", colorama.Fore.GREEN],
        "cogs_negative":["COGS", colorama.Fore.RED],
        "cogs_other":["COGS", colorama.Fore.CYAN],
        "bot":["BOT", colorama.Fore.BLUE],
        "debug":["DEBUG", colorama.Fore.MAGENTA],
        "error":["ERROR", colorama.Fore.LIGHTRED_EX]
    }
    result = f"{prefixes[prefix][1]}\033[1m[{prefixes[prefix][0]}]\033[0m{colorama.Fore.WHITE}"
    return result