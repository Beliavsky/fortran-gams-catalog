! GAMS H2a1b2. Unweighted polynomial quadrature on [-1,1].
program check_cheb_quadrature
  implicit none
  interface
    subroutine chebexps(itype,n,x,u,v,w)
      integer :: itype,n
      real(kind=8) :: x(*),u(n,n),v(n,n),w(*)
    end subroutine
  end interface
  integer,parameter :: orders(4)=[2,4,8,16]
  real(kind=8),allocatable :: x(:),w(:),u(:,:),v(:,:)
  real(kind=8) :: exact,error,maxerr
  integer :: n,i,k,cases
  cases=0; maxerr=0d0
  do i=1,size(orders)
    n=orders(i)
    allocate(x(n),w(n),u(n,n),v(n,n))
    call chebexps(1,n,x,u,v,w)
    if(.not.all(x(2:n)>x(1:n-1)))error stop 'nodes not ascending'
    if(.not.all(abs(x)<1d0))error stop 'nodes outside open interval'
    if(.not.all(w>0d0))error stop 'weights not positive'
    do k=0,n-1
      exact=0d0
      if(mod(k,2)==0)exact=2d0/real(k+1,8)
      error=abs(sum(w*x**k)-exact)
      if(.not.(error<2d-13))error stop 'unweighted polynomial moment failed'
      maxerr=max(maxerr,error); cases=cases+1
    enddo
    deallocate(x,w,u,v)
  enddo
  print '(a,i0)','Polynomial moments checked: ',cases
  print '(a,es12.4)','Maximum absolute moment error: ',maxerr
  print '(a)','PASS Chebyshev-node quadrature: 30 moments and node/weight checks'
end program check_cheb_quadrature
