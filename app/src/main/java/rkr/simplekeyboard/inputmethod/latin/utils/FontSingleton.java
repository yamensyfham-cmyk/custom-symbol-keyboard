package rkr.simplekeyboard.inputmethod.latin.utils;

import android.content.Context;
import android.graphics.Typeface;

public final class FontSingleton {
    private static Typeface sSymbolsTypeface;
    private static Typeface sMathTypeface;

    private FontSingleton() {}

    public static Typeface getSymbolsTypeface(Context context) {
        if (sSymbolsTypeface == null) {
            try {
                sSymbolsTypeface = Typeface.createFromAsset(
                        context.getAssets(), "fonts/NotoSansSymbols2-Regular.ttf");
            } catch (Exception e) {
                sSymbolsTypeface = Typeface.DEFAULT;
            }
        }
        return sSymbolsTypeface;
    }

    public static Typeface getMathTypeface(Context context) {
        if (sMathTypeface == null) {
            try {
                sMathTypeface = Typeface.createFromAsset(
                        context.getAssets(), "fonts/NotoSansMath-Regular.ttf");
            } catch (Exception e) {
                sMathTypeface = Typeface.DEFAULT;
            }
        }
        return sMathTypeface;
    }

    public static void clear() {
        sSymbolsTypeface = null;
        sMathTypeface = null;
    }
}
