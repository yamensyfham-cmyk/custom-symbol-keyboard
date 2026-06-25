package rkr.simplekeyboard.inputmethod.keyboard;

import android.content.Context;
import android.content.SharedPreferences;

import java.util.Locale;

import rkr.simplekeyboard.inputmethod.compat.PreferenceManagerCompat;

public final class SymbolKeyboardManager {
    private static final String KEY_CURRENT_PAGE = "current_symbol_page";
    private static final int TOTAL_PAGES = 112;
    private static int sStaticCurrentPage = 0;

    private static SymbolKeyboardManager sInstance;
    private final SharedPreferences mPrefs;
    private int mCurrentPage;

    private SymbolKeyboardManager(Context context) {
        mPrefs = PreferenceManagerCompat.getDeviceSharedPreferences(context);
        mCurrentPage = mPrefs.getInt(KEY_CURRENT_PAGE, 0);
        if (mCurrentPage < 0 || mCurrentPage >= TOTAL_PAGES) {
            mCurrentPage = 0;
        }
        sStaticCurrentPage = mCurrentPage;
    }

    public static SymbolKeyboardManager getInstance(Context context) {
        if (sInstance == null) {
            sInstance = new SymbolKeyboardManager(context.getApplicationContext());
        }
        return sInstance;
    }

    public static int getStaticCurrentPage() {
        return sStaticCurrentPage;
    }

    public int getCurrentPage() {
        return mCurrentPage;
    }

    public int getTotalPages() {
        return TOTAL_PAGES;
    }

    public boolean hasNextPage() {
        return mCurrentPage < TOTAL_PAGES - 1;
    }

    public boolean hasPrevPage() {
        return mCurrentPage > 0;
    }

    public int nextPage() {
        if (mCurrentPage < TOTAL_PAGES - 1) {
            mCurrentPage++;
            sStaticCurrentPage = mCurrentPage;
            save();
        }
        return mCurrentPage;
    }

    public int prevPage() {
        if (mCurrentPage > 0) {
            mCurrentPage--;
            sStaticCurrentPage = mCurrentPage;
            save();
        }
        return mCurrentPage;
    }

    public int goToPage(int page) {
        if (page >= 0 && page < TOTAL_PAGES) {
            mCurrentPage = page;
            sStaticCurrentPage = mCurrentPage;
            save();
        }
        return mCurrentPage;
    }

    public static final boolean USE_PAGED_MODE = true;

    public String getPageName() {
        return String.format(Locale.US, "sym_page_%04d", mCurrentPage);
    }

    public String getPageNameForPage(int page) {
        return String.format(Locale.US, "sym_page_%04d", page);
    }

    private void save() {
        mPrefs.edit().putInt(KEY_CURRENT_PAGE, mCurrentPage).apply();
    }
}
