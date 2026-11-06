! Catalog-owned analytic checks of GAMS E3a2 using CHEBINMT.
! Upstream source is downloaded at a pinned revision; it is not bundled here.
program derivative
 use iso_fortran_env, only: real64
 use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
 implicit none
 integer :: n,k,j,count
 real(real64), allocatable :: x(:),weights(:),u(:,:),v(:,:),a(:,:),d(:,:),w(:),ending(:),values(:),want(:),got(:)
 real(real64) :: error,maximum,endpoint
 real(real64), parameter :: tolerance=2.e-11_real64
 external :: chebexps,chebinmt
 maximum=0
 count=0
 do j=1,4
   n=2**j
   allocate(x(n),weights(n),u(n,n),v(n,n),a(n,n),d(n,n),w(3*n*n+2*n+50), &
      ending(n),values(n),want(n),got(n))
   call chebinmt(n,a,d,x,weights,ending,2,w)
   do k=0,n-1
     values=x**k
     got=matmul(d,values)
     want=0
     if(k>0) want=real(k,real64)*x**(k-1)
     call verify()
     endpoint=dot_product(ending,values)
     if(.not.ieee_is_finite(endpoint)) error stop 'nonfinite endpoint'
     if(abs(endpoint-1._real64)>tolerance) error stop 'endpoint mismatch'
   end do
   deallocate(x,weights,u,v,a,d,w,ending,values,want,got)
 end do
 print '(a,i0)', 'Checked polynomial cases: ',count
 print '(a,es14.6)', 'Maximum normalized error: ',maximum
 print '(a)', 'PASS derivative'
contains
 subroutine verify()
   if(.not.all(ieee_is_finite(got))) error stop 'nonfinite result'
   error=maxval(abs(got-want))/max(1._real64,maxval(abs(want)))
   maximum=max(maximum,error)
   if(error>tolerance) error stop 'analytic polynomial mismatch'
   count=count+1
 end subroutine
end program
