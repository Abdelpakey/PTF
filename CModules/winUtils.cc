#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"

#include <windows.h>
#include <Python.h>
#include <numpy/arrayobject.h>

using namespace std;

static PyObject* hideBorder(PyObject* self, PyObject* args);
static PyObject* hideBorder2(PyObject* self, PyObject* args);
static PyObject* loseFocus(PyObject* self, PyObject* args);
static PyObject* show(PyObject* self, PyObject* args);
static PyObject* show2(PyObject* self, PyObject* args);

static PyMethodDef winUtilsMethods[] = {
	{ "hideBorder", hideBorder, METH_VARARGS },
	{ "hideBorder2", hideBorder2, METH_VARARGS },
	{ "loseFocus", loseFocus, METH_VARARGS },
	{ "show", show, METH_VARARGS },
	{ "show2", show2, METH_VARARGS },
	{ NULL, NULL, 0, NULL }     /* Sentinel - marks the end of this structure */
};

#if PY_MAJOR_VERSION < 3
PyMODINIT_FUNC initwinUtils() {
	(void)Py_InitModule("winUtils", winUtilsMethods);
	import_array();  // Must be present for NumPy.  Called first after above line.
}
#else
static struct PyModuleDef winUtilsModule = {
	PyModuleDef_HEAD_INIT,
	"winUtils",   /* name of module */
	NULL, /* module documentation, may be NULL */
	-1,       /* size of per-interpreter state of the module,
			  or -1 if the module keeps state in global variables. */
	winUtilsMethods
};
PyMODINIT_FUNC PyInit_winUtils(void) {
	import_array();
	return PyModule_Create(&winUtilsModule);
}
#endif


static PyObject* hideBorder(PyObject* self, PyObject* args) {
	char* win_name;
	int x, y, w, h;
	if(!PyArg_ParseTuple(args, "iiiiz", &x, &y, &w, &h, &win_name)) {
		PySys_WriteStdout("\n----winUtils::create: Input arguments could not be parsed----\n\n");
		return Py_BuildValue("i", 0);
	}
	HWND win_handle = FindWindow(0, win_name);
	if(!win_handle) {
		PySys_WriteStdout("Failed FindWindow\n");
		return Py_BuildValue("i", 0);
	}

	printf("x: %d\n", x);
	printf("y: %d\n", y);
	printf("w: %d\n", w);
	printf("h: %d\n", h);

	// Resize
	unsigned int flags = (SWP_SHOWWINDOW | SWP_NOSIZE | SWP_NOZORDER);
	flags &= ~SWP_NOSIZE;
	SetWindowPos(win_handle, HWND_TOPMOST, x, y, w, h, flags);

	// Borderless
	SetWindowLong(win_handle, GWL_STYLE, GetWindowLong(win_handle, GWL_EXSTYLE) | WS_EX_TOPMOST);

	return Py_BuildValue("i", 1);
}

static PyObject* hideBorder2(PyObject* self, PyObject* args) {
	char* win_name;
	if(!PyArg_ParseTuple(args, "z", &win_name)) {
		PySys_WriteStdout("\n----winUtils::hideBorder2: Input arguments could not be parsed----\n\n");
		return Py_BuildValue("i", 0);
	}
	HWND win_handle = FindWindow(0, win_name);
	if(!win_handle) {
		PySys_WriteStdout("Failed FindWindow\n");
		return Py_BuildValue("i", 0);
	}
	// change style of the child HighGui window
	DWORD style = ::GetWindowLong(win_handle, GWL_STYLE);
	style &= ~WS_OVERLAPPEDWINDOW;
	style |= WS_POPUP;
	style |= WS_EX_TOPMOST;
	::SetWindowLong(win_handle, GWL_STYLE, style);

	// change style of the parent HighGui window
	HWND hParent = ::FindWindow(0, win_name);
	style = ::GetWindowLong(hParent, GWL_STYLE);
	style &= ~WS_OVERLAPPEDWINDOW;
	style |= WS_POPUP;
	style |= WS_EX_TOPMOST;
	::SetWindowLong(hParent, GWL_STYLE, style);
	return Py_BuildValue("i", 1);
}

static PyObject* loseFocus(PyObject* self, PyObject* args) {
	char* win_name;
	if(!PyArg_ParseTuple(args, "z", &win_name)) {
		PySys_WriteStdout("\n----winUtils::loseFocus: Input arguments could not be parsed----\n\n");
		return Py_BuildValue("i", 0);
	}
	HWND win_handle = FindWindow(0, win_name);
	if(!win_handle) {
		PySys_WriteStdout("Failed FindWindow\n");
		return Py_BuildValue("i", 0);
	}
	SetWindowPos(win_handle, HWND_NOTOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE);

	return Py_BuildValue("i", 1);
}

auto ConvertCVMatToBMP(const cv::Mat &frame) -> HBITMAP
{
	auto convertOpenCVBitDepthToBits = [](const int32_t value)
	{
		auto regular = 0u;

		switch(value)
		{
		case CV_8U:
		case CV_8S:
			regular = 8u;
			break;

		case CV_16U:
		case CV_16S:
			regular = 16u;
			break;

		case CV_32S:
		case CV_32F:
			regular = 32u;
			break;

		case CV_64F:
			regular = 64u;
			break;

		default:
			regular = 0u;
			break;
		}

		return regular;
	};

	auto imageSize = frame.size();
	assert(imageSize.width && "invalid size provided by frame");
	assert(imageSize.height && "invalid size provided by frame");

	if(imageSize.width && imageSize.height)
	{
		auto headerInfo = BITMAPINFOHEADER{};
		ZeroMemory(&headerInfo, sizeof(headerInfo));

		headerInfo.biSize = sizeof(headerInfo);
		headerInfo.biWidth = imageSize.width;
		headerInfo.biHeight = -(imageSize.height); // negative otherwise it will be upsidedown
		headerInfo.biPlanes = 1;// must be set to 1 as per documentation frame.channels();

		const auto bits = convertOpenCVBitDepthToBits(frame.depth());
		headerInfo.biBitCount = frame.channels() * bits;

		auto bitmapInfo = BITMAPINFO{};
		ZeroMemory(&bitmapInfo, sizeof(bitmapInfo));

		bitmapInfo.bmiHeader = headerInfo;
		bitmapInfo.bmiColors->rgbBlue = 0;
		bitmapInfo.bmiColors->rgbGreen = 0;
		bitmapInfo.bmiColors->rgbRed = 0;
		bitmapInfo.bmiColors->rgbReserved = 0;

		auto dc = GetDC(nullptr);
		assert(dc != nullptr && "Failure to get DC");
		auto bmp = CreateDIBitmap(dc,
			&headerInfo,
			CBM_INIT,
			frame.data,
			&bitmapInfo,
			DIB_RGB_COLORS);
		assert(bmp != nullptr && "Failure creating bitmap from captured frame");

		return bmp;
	} else
	{
		return nullptr;
	}
}

static PyObject* show(PyObject* self, PyObject* args) {
	char* win_name;
	PyArrayObject *img_py;
	int mode;
	if(!PyArg_ParseTuple(args, "zO!i", &win_name, &PyArray_Type, &img_py, &mode)) {
		PySys_WriteStdout("\n----winUtils::show: Input argument could not be parsed----\n\n");
		return Py_BuildValue("i", 0);
	}
	if(img_py == NULL) {
		PySys_WriteStdout("\n----winUtils::show::img_py is NULL----\n\n");
		return Py_BuildValue("i", 0);
	}
	int img_height = img_py->dimensions[0];
	int img_width = img_py->dimensions[1];
	int n_channels = img_py->nd == 3 ? img_py->dimensions[2] : 1;

	if(n_channels != 1 && n_channels != 3) {
		PySys_WriteStdout("pyMTF:: Only grayscale and RGB images are supported\n");
		return Py_BuildValue("i", 0);
	}

	int img_type = n_channels == 3 ? CV_8UC3 : CV_8UC1;
	cv::Mat img_cv(img_height, img_width, img_type, img_py->data);

	if(mode == 0) {
		cv::imshow(win_name, img_cv);
	} else {
		HWND win_handle = FindWindow(0, win_name);
		if(!win_handle) {
			PySys_WriteStdout("Failed FindWindow\n");
			return Py_BuildValue("i", 0);
		}
		auto hBitmap = ConvertCVMatToBMP(img_cv);
		if(!hBitmap) {
			PySys_WriteStdout("Image conversion to hBitmap failed\n");
			return Py_BuildValue("i", 0);
		}

		if(mode == 1) {
			PAINTSTRUCT     ps;
			HDC             hdc;
			BITMAP          bitmap;
			HDC             hdcMem;
			HGDIOBJ         oldBitmap;

			hdc = BeginPaint(win_handle, &ps);

			hdcMem = CreateCompatibleDC(hdc);
			oldBitmap = SelectObject(hdcMem, hBitmap);

			GetObject(hBitmap, sizeof(bitmap), &bitmap);
			BitBlt(hdc, 0, 0, bitmap.bmWidth, bitmap.bmHeight, hdcMem, 0, 0, SRCCOPY);

			SelectObject(hdcMem, oldBitmap);
			DeleteDC(hdcMem);

			EndPaint(win_handle, &ps);
		} else {
			RECT rect;
			HDC hdc = GetDC(win_handle);
			HBRUSH brush = CreatePatternBrush(hBitmap);
			GetWindowRect(win_handle, &rect);
			FillRect(hdc, &rect, brush);
			DeleteObject(brush);
			ReleaseDC(win_handle, hdc);
		}
		ShowWindow(win_handle, SW_SHOW);
	}
	return Py_BuildValue("i", 1);
}

static PyObject* show2(PyObject* self, PyObject* args) {
	char* win_name;
	if(!PyArg_ParseTuple(args, "z", &win_name)) {
		PySys_WriteStdout("\n----winUtils::show: Input argument could not be parsed----\n\n");
		return Py_BuildValue("i", 0);
	}
	HWND win_handle = FindWindow(0, win_name);
	if(!win_handle) {
		PySys_WriteStdout("Failed FindWindow\n");
		return Py_BuildValue("i", 0);
	}
	ShowWindow(win_handle, SW_SHOW);
	return Py_BuildValue("i", 1);
}
