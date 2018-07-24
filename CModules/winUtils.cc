#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"

#include <windows.h>
#include <Python.h>
#include <numpy/arrayobject.h>

using namespace std;

static PyObject* hideBorder(PyObject* self, PyObject* args);
static PyObject* hideBorder2(PyObject* self, PyObject* args);

static PyMethodDef winUtilsMethods[] = {
	{ "hideBorder", hideBorder, METH_VARARGS },
	{ "hideBorder2", hideBorder2, METH_VARARGS },
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
	unsigned int flags = (SWP_SHOWWINDOW | SWP_NOSIZE | SWP_NOMOVE | SWP_NOZORDER);
	flags &= ~SWP_NOSIZE;
	SetWindowPos(win_handle, HWND_TOPMOST, x, y, w, h, flags);

	// Borderless
	SetWindowLong(win_handle, GWL_STYLE, GetWindowLong(win_handle, GWL_EXSTYLE) | WS_EX_TOPMOST);
	ShowWindow(win_handle, SW_SHOW);

	return Py_BuildValue("i", 1);
}


static PyObject* hideBorder2(PyObject* self, PyObject* args) {
	char* win_name;
	if(!PyArg_ParseTuple(args, "z", &win_name)) {
		PySys_WriteStdout("\n----winUtils::create: Input arguments could not be parsed----\n\n");
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
	::SetWindowLong(win_handle, GWL_STYLE, style);

	// change style of the parent HighGui window
	HWND hParent = ::FindWindow(0, win_name);
	style = ::GetWindowLong(hParent, GWL_STYLE);
	style &= ~WS_OVERLAPPEDWINDOW;
	style |= WS_POPUP;
	::SetWindowLong(hParent, GWL_STYLE, style);

	return Py_BuildValue("i", 1);
}
