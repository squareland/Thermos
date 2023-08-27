package thermos;

import java.util.HashMap;

import cpw.mods.fml.common.network.FMLEmbeddedChannel;
import cpw.mods.fml.common.network.FMLOutboundHandler;
import cpw.mods.fml.common.network.NetworkRegistry;
import cpw.mods.fml.relauncher.Side;
import io.netty.channel.ChannelFutureListener;
import net.minecraft.entity.player.EntityPlayerMP;
import net.minecraftforge.common.DimensionManager;
import net.minecraftforge.common.network.ForgeMessage;

public class VoidFlame {

	// Note: These fields are accessible so that plugins can easily control the values
	public static boolean disableFluidFlowEvent;
	public static boolean disableMobSpawning;
	public static boolean disableEntityAI;
	public static HashMap<Class<?>, Integer> bannedTiles = new HashMap<Class<?>, Integer>(); //Class -> Meta

	// This isn't currently used
	private static void sendDimensionRegisterPacket(EntityPlayerMP player, int dimensionID) {
		System.out.println("[Thermos] Send DimensionRegisterMessage to " + player.getDisplayName() + " :: " + dimensionID);
		int providerID = DimensionManager.getProviderType(dimensionID);
		ForgeMessage msg = new ForgeMessage.DimensionRegisterMessage(dimensionID, providerID);
		// FMLEmbeddedChannel channel = ForgeNetworkHandler.getServerChannel();
		// NetworkRegistry.INSTANCE.getChannel("FORGE", Side.SERVER);
		FMLEmbeddedChannel channel = NetworkRegistry.INSTANCE.getChannel("FORGE", Side.SERVER);
		channel.attr(FMLOutboundHandler.FML_MESSAGETARGET).set(FMLOutboundHandler.OutboundTarget.PLAYER);
		channel.attr(FMLOutboundHandler.FML_MESSAGETARGETARGS).set(player);
		channel.writeAndFlush(msg).addListener(ChannelFutureListener.FIRE_EXCEPTION_ON_FAILURE);
	}

}
