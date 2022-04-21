package moe.rebuild.myrai;

import net.mamoe.mirai.event.ListeningStatus;
import net.mamoe.mirai.event.events.MessageEvent;

public interface PyListenerHost {
    void onMessage(MessageEvent event);

    default void handleException(Throwable exception) {}

    default ListeningStatus onMessageWithStat(MessageEvent event) {
        return ListeningStatus.LISTENING;
    }
}
