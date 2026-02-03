import threading

from windows_toasts import (
    InteractableWindowsToaster, 
    Toast,
    ToastActivatedEventArgs, 
    ToastDisplayImage, 
    ToastImage, 
    ToastProgressBar,
    ToastImagePosition,
    ToastButton
)

toaster = InteractableWindowsToaster('OpenTwitchLive')
image = ToastImage(imagePath='./assets/twitch.png') 

newToast = Toast(['Starting.'])
newToast.AddAction(ToastButton('Open Twitch', 'open_twitch'))
newToast.AddAction(ToastButton('Close', 'close'))

newToast.images = [
    ToastDisplayImage(image, position=ToastImagePosition.AppLogo)
]

stop_event = threading.Event()
should_open_browser = True

def activated_callback(activated_event_args: ToastActivatedEventArgs):
    global should_open_browser
    args = activated_event_args.arguments
    
    if args == 'open_twitch':
        should_open_browser = True
        stop_event.set()
        
    elif args == 'close':
        should_open_browser = False
        stop_event.set()

newToast.on_activated = activated_callback

def show_timed_toast(message: str, seconds: int = 10) -> bool:
    """
    Mostra il toast con countdown.
    Ritorna True se bisogna aprire il sito, False se l'utente ha annullato.
    """
    global should_open_browser
    
    stop_event.clear()
    should_open_browser = True
    
    progress_bar = ToastProgressBar('Progress', None, 0.0)
    progress_bar.progress = 1.0
    newToast.progress_bar = progress_bar
    
    newToast.text_fields = [message, f'Opening in {seconds} seconds...']
    toaster.show_toast(newToast)

    for remaining in range(seconds, 0, -1):
        if stop_event.is_set():
            break
            
        newToast.text_fields = [message, f'Opening in {remaining} seconds...']
        newToast.progress_bar.progress = (seconds - remaining) / seconds
        toaster.update_toast(newToast)
        
        if stop_event.wait(1.0): 
            break

    toaster.remove_toast(newToast)
    
    return should_open_browser

def show_fail_toast(message: str, seconds: int = 5):
    fail_toast = Toast([message])
    fail_toast.images = [
        ToastDisplayImage(image, position=ToastImagePosition.AppLogo)
    ]
    
    toaster.show_toast(fail_toast)
    threading.Timer(seconds, lambda: toaster.remove_toast(fail_toast)).start()