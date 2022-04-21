package moe.rebuild.myrai;

import kotlin.coroutines.CoroutineContext;
import net.mamoe.mirai.event.EventHandler;
import net.mamoe.mirai.event.ListeningStatus;
import net.mamoe.mirai.event.SimpleListenerHost;
import net.mamoe.mirai.event.events.MessageEvent;

public class MyraiListenerHost extends SimpleListenerHost {
    private PyListenerHost pyListenerHost;

    public MyraiListenerHost(PyListenerHost h) {
        this.pyListenerHost = h;
    }

    @Override
    public void handleException(CoroutineContext context, Throwable exception) {
        pyListenerHost.handleException(exception);
    }

    @EventHandler
    public void onMessage(MessageEvent event) throws Exception {
        pyListenerHost.onMessage(event);
    }

    @EventHandler
    public ListeningStatus onMessageWithStatus(MessageEvent event) throws Exception {
        return pyListenerHost.onMessageWithStat(event);
    }
}
