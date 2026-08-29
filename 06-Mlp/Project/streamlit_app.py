import os
import numpy as np
import streamlit as st
from PIL import Image, ImageFilter
from scipy import ndimage
from tensorflow import keras

st.set_page_config(page_title="Digit Recognizer")
st.title("Handwritten Digit Recognizer")

# ---------------------------------------------------------------------------
# CHANGE THIS to the model you downloaded from Colab.
# In Colab: run the save cell, then download my_first_trained_model.keras,
# and paste the full path to it here.
MODEL_PATH = "/home/leapfrog/Downloads/my_first_trained_model_3.keras"
# ---------------------------------------------------------------------------

if not os.path.exists(MODEL_PATH):
    st.error(f"No model file at `{MODEL_PATH}`")
    st.info(
        "Open `app_test.py`, find the `MODEL_PATH` line near the top, and set it to "
        "the full path of the `.keras` file you downloaded from Colab.\n\n"
        "On Linux or Mac it usually looks like `/home/you/Downloads/my_first_trained_model.keras`, "
        "on Windows like `C:/Users/you/Downloads/my_first_trained_model.keras`."
    )
    st.stop()

model = keras.models.load_model(MODEL_PATH)


def prepare_image(pil_image):
    """Turn a photo of a handwritten digit into the 28x28 input the model expects.

    A phone photo looks nothing like MNIST, so there is real work to do here.
    """
    gray = pil_image.convert("L")
    a = np.asarray(gray, dtype=np.float32)
    big = max(gray.size)

    def ink(radius):
        """Whatever is DARKER than its own local background is ink.

        Blurring the photo estimates what the blank page looks like: the blur
        erases the pen strokes but keeps shadows and uneven lighting. Comparing
        against that also handles the inversion, since a photo is dark ink on
        white paper while MNIST is a white digit on black.
        """
        bg = np.asarray(gray.filter(ImageFilter.GaussianBlur(radius)), dtype=np.float32)
        return np.clip(bg - a, 0, None)

    # The blur radius has to be bigger than the pen stroke, or the "background"
    # eats into the stroke and hollows it out. But too big and it stops tracking
    # a sharp shadow edge. So measure the stroke first, then size the radius to it.
    rough = ink(big / 12.0)
    if rough.max() == 0:
        return np.zeros((28, 28), np.float32)
    rough_mask = rough > 0.4 * rough.max()
    if not rough_mask.any():
        return np.zeros((28, 28), np.float32)
    stroke = 2.0 * np.percentile(
        ndimage.distance_transform_edt(rough_mask)[rough_mask], 90
    )
    a = ink(float(np.clip(3.0 * stroke, big / 60.0, big / 3.0)))

    if a.max() == 0:
        return np.zeros((28, 28), np.float32)

    # Keep only the biggest connected blob of ink. That is the digit - ruled
    # paper lines, smudges and dust specks get dropped here.
    mask = a > 0.35 * a.max()
    labels, n = ndimage.label(mask)
    if n > 1:
        sizes = ndimage.sum(mask, labels, range(1, n + 1))
        mask = labels == (1 + int(np.argmax(sizes)))
    if not mask.any():
        return np.zeros((28, 28), np.float32)

    # Crop tight to the digit, then rebuild the MNIST framing ourselves: scale the
    # longest side to 20px and paste it centred into a 28x28 box. Taking the margin
    # from the photo instead would fail whenever someone zooms right in.
    ys, xs = np.where(mask)
    a = a[ys.min() : ys.max() + 1, xs.min() : xs.max() + 1]
    a = a / a.max() * 255.0

    h, w = a.shape
    scale = 20.0 / max(h, w)
    nh, nw = max(1, int(round(h * scale))), max(1, int(round(w * scale)))
    small = np.asarray(
        Image.fromarray(a.astype(np.uint8)).resize((nw, nh), Image.LANCZOS),
        dtype=np.float32,
    )

    out = np.zeros((28, 28), np.float32)
    top, left = (28 - nh) // 2, (28 - nw) // 2
    out[top : top + nh, left : left + nw] = small

    # MNIST digits sit at their centre of mass, not the centre of their box.
    total = out.sum()
    if total > 0:
        idx = np.arange(28)
        dy = int(round(13.5 - out.sum(1) @ idx / total))
        dx = int(round(13.5 - out.sum(0) @ idx / total))
        shifted = np.zeros_like(out)
        y0, y1 = max(0, dy), 28 + min(0, dy)
        x0, x1 = max(0, dx), 28 + min(0, dx)
        shifted[y0:y1, x0:x1] = out[y0 - dy : y1 - dy, x0 - dx : x1 - dx]
        out = shifted

    return out / max(out.max(), 1e-6)


# Upload image
# The uploader's key includes a counter. Bumping the counter gives Streamlit a
# brand new widget, which is how we clear the current file and ask for another.
if "upload_round" not in st.session_state:
    st.session_state.upload_round = 0

st.caption("Take a photo of a handwritten digit (0-9) and upload it.")
image_file = st.file_uploader(
    "Upload digit image",
    type=["png", "jpg", "jpeg"],
    key=f"digit_image_{st.session_state.upload_round}",
)

if image_file is not None:
    img_array = prepare_image(Image.open(image_file))

    left, right = st.columns(2)

    with left:
        st.image(Image.open(image_file), caption="Your image", width=250)

    with right:
        y_prob = model.predict(img_array.reshape(1, 28, 28), verbose=0)[0]
        y_pred = y_prob.argmax()
        st.markdown(f"# Predicted: {y_pred}")
        st.progress(float(y_prob[y_pred]), text=f"{y_prob[y_pred]:.1%} confident")

    st.bar_chart({"probability": y_prob})

    with st.expander("What the model sees (28x28)"):
        st.caption(
            "This should be a white digit on a black background. "
            "If it is not, the prediction will be wrong."
        )
        st.image(img_array, width=140, clamp=True)

    if st.button("Upload another image", type="primary"):
        st.session_state.upload_round += 1
        st.rerun()
